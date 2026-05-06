import io
import json
import math

import numpy as np
import torch
from fastapi import FastAPI, HTTPException, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image

from config import get_config
from vae import VAE

cfg = get_config()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = VAE(cfg.channels, cfg.hidden_dim, cfg.latent_dim, cfg.encoder_dropout)
model.load_state_dict(torch.load("./checkpoints/best_model.pt", map_location=device)["model_state"])
model.to(device)
model.eval()

with open("./latent_distributions/pokemon_distributions.json") as f:
    dist_dict = json.load(f)


def get_mean(pokemon_id: int) -> torch.Tensor:
    entry = dist_dict.get(str(pokemon_id))
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Pokemon id {pokemon_id} not found")
    return torch.tensor(entry["mean"], dtype=torch.float32, device=device)


def interpolate_latent(id1: int, id2: int, alpha: float) -> torch.Tensor:
    if alpha <= 0.0:
        return get_mean(id1)
    if alpha >= 1.0:
        return get_mean(id2)

    mu1 = get_mean(id1)
    mu2 = get_mean(id2)

    v0 = mu1 / torch.norm(mu1)
    v1 = mu2 / torch.norm(mu2)

    theta = math.acos(torch.dot(v0, v1).clamp(-1.0, 1.0).item())

    if theta < 1e-6:
        return (1.0 - alpha) * mu1 + alpha * mu2

    return (math.sin((1.0 - alpha) * theta) / math.sin(theta)) * mu1 + \
           (math.sin(alpha * theta) / math.sin(theta)) * mu2


def decode_latent(z: torch.Tensor) -> torch.Tensor:
    with torch.no_grad():
        return model.decoder(z.unsqueeze(0))  # [1, 4, 96, 96]


def tensor_to_png_bytes(tensor: torch.Tensor) -> bytes:
    # tensor: [1, 4, 96, 96], values in [0, 1] from Sigmoid
    arr = tensor.squeeze(0).permute(1, 2, 0).cpu().numpy()  # [96, 96, 4]
    arr = (arr * 255).clip(0, 255).astype(np.uint8)
    image = Image.fromarray(arr, mode="RGBA")
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    return buf


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.post("/interpolate")
async def interpolate(
    pokedex_id_1: int = Query(...),
    pokedex_id_2: int = Query(...),
    alpha: float = Query(..., ge=0.0, le=1.0),
    x_api_key: str = Header(...)
):
    z = interpolate_latent(pokedex_id_1, pokedex_id_2, alpha)
    tensor = decode_latent(z)
    buf = tensor_to_png_bytes(tensor)
    return StreamingResponse(buf, media_type="image/png")
