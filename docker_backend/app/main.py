from fastapi import FastAPI
from pydantic import BaseModel
from vae import VAE
import torch
from config import get_config

cfg = get_config()
model = VAE(cfg.channels, cfg.hidden_dim, cfg.latent_dim)
model.load_state_dict(torch.load("./checkpoints/best_model.pt"))

class DecodeRequest(BaseModel):
    embedding: list[float]  # FastAPI validates this is a list of floats

app = FastAPI()

@app.post("/decode")
async def decode(req: DecodeRequest):
    # by the time you're here, req.embedding is guaranteed valid
    result = (req.embedding)
    return result