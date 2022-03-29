#!/bin/bash
#
#SBATCH --job-name=sp_n1000_0_600_b
#SBATCH --partition=gpu
#SBATCH --gpus=4
#SBATCH --cpus-per-task=16
#SBATCH --mem=1GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

/usr/bin/time ../align_database.py data/sp_n1000_0_600_b -p ssw swipe adept