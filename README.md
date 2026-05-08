# PokAE Interpolator

[Live App](https://brave-water-0f1e3a510.7.azurestaticapps.net/) · [GitHub](https://github.com/brybranmuffin/gen_ai_image_project)

## Overview

PokAE Interpolator is an application that allows users to explore what it would look like if they combined their two favorite Pokémon together. It uses a Variational Autoencoder (VAE) to encode latent representations of nearly all 1,025 different species of currently discovered Pokémon. PokAE Interpolator uses spherical linear interpolation (SLERP) to smoothly combine the encoded features of each Pokémon, generating hours of exploration and fun for the user.

![PokAE Interpolator example](example_interpolation.png)

## Extra Criteria - Gallery UI

- **Novel interpolation UI** — A custom slider-based interface lets users select two Pokémon and control the interpolation weight between them in real time, generating a fused image on demand.
- **Azure hosting** — The application is fully deployed on Azure, with the inference backend running as a containerized FastAPI service behind Azure API Management, and the frontend hosted on Azure Static Web Apps.
- **Fusion gallery** — The application includes a curated gallery of generated fusion examples to give users an idea of what interpolated images look like before they start exploring on their own.

## Difficulties

### Image Data Issues

- The current application was trained on all Pokémon except **#698 — Tyrunt**. The source image was corrupted and could not be recovered, so Tyrunt was excluded from the dataset.
- Training loss plateaued around epoch 300 and showed no meaningful improvement through at least epoch 500. On re-examining the training pipeline, it became clear that augmenting images offline (pre-generating copies before training) rather than sampling augmentations dynamically at training time was likely a contributing factor. The pipeline was updated to sample augmented views from raw sprites at training time, but the loss did not improve further, suggesting the model had reached its capacity ceiling for this dataset size.

### Interpolated Image Quality

Linear interpolation was the initial approach for combining latent vectors, but the quality and feature blending between distant Pokémon were lacking. Switching to spherical linear interpolation (SLERP) improved image sharpness slightly in some cases by interpolating along the surface of the latent space rather than cutting straight through it.

### Azure and Docker Deployment

Several issues came up when learning to deploy the Docker image to Azure and connecting Azure Container Apps to API Management. All in all, not a difficult project for this level of application.

## How to run
App is hosted on Azure Static Web Apps. Model is hosted on Azure Container Instance. You can find the app here: https://brave-water-0f1e3a510.7.azurestaticapps.net/

### Building Files Locally
Currently there is no way to run the entire application locally. Front end code is configured to use hosted Azure API for interpolation requests. 

1. Building and Testing Backend

To run the backend locally we first have to build the docker image and then start the container.

```bash
docker build -t pokae_backend .
```

2. Running Frontend

```bash
cd ../frontend
npm run start
```

## VAE Development

### Data Sources
### Model Architecture
### Training Results

## Application Architecture

