# PokAEmon Project

### Variational Autoencoder project trained on pokemon sprites to generate new pokemon images by interpolating between two existing pokemon images.

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