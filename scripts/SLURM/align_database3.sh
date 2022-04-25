#!/bin/bash
#
#SBATCH --job-name=sp_n1000
#SBATCH --partition=gpu
#SBATCH --gpus=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=20GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

/usr/bin/time ../align_database.py data/sp_n1000_10_500
/usr/bin/time ../align_database.py data/sp_n1000_10_1000
/usr/bin/time ../align_database.py data/sp_n1000_501_1000