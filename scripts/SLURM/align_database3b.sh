#!/bin/bash
#
#SBATCH --job-name=sp_n1000_b
#SBATCH --partition=gpu
#SBATCH --gpus=4
#SBATCH --cpus-per-task=12
#SBATCH --mem=20GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

/usr/bin/time ../align_database.py data/sp_n1000_10_500_b -t 12 -g 4 
/usr/bin/time ../align_database.py data/sp_n1000_10_1000_b -t 12 -g 4 
/usr/bin/time ../align_database.py data/sp_n1000_501_1000_b -t 12 -g 4 