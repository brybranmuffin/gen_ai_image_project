#!/bin/bash
#SBATCH --account=e32706       # replace with your Quest allocation ID
#SBATCH --partition=gengpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:a100:1
#SBATCH --mem=32G
#SBATCH --time=08:00:00
#SBATCH --job-name=pokemon_vae
#SBATCH --output=../logs/slurm_%j.out
#SBATCH --error=../logs/slurm_%j.err

module purge
module load python/anaconda3
source activate scpmnet

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/checkpoints"

cd "$PROJECT_DIR/model_scripts"

python train.py \
    --data_dir         "$PROJECT_DIR/data" \
    --checkpoint_dir   "$PROJECT_DIR/checkpoints" \
    --log_dir          "$PROJECT_DIR/logs" \
    --latent_dim       128 \
    --hidden_dim       512 \
    --beta             1.0 \
    --batch_size       64 \
    --epochs           100 \
    --learning_rate    1e-3 \
    --num_workers      4 \
    --save_every       10
