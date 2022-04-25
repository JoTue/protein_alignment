#!/bin/bash
#
#SBATCH --job-name=adept_t1g1
#SBATCH --partition=gpu
#SBATCH --gpus=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=10GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

/usr/bin/time ../program_scripts/adept.py data/sp_n8000_10_600
/usr/bin/time ../program_scripts/adept_as.py data/sp_n8000_10_600