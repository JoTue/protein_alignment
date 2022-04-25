#!/bin/bash
#
#SBATCH --job-name=cudasw_xargs
#SBATCH --partition=gpu
#SBATCH --gpus=3
#SBATCH --cpus-per-task=3
#SBATCH --mem=10GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 100000000
/usr/bin/time ../align_database.py data/sp_n400_0_600 -r -p cudasw_xargs -t 3 -g 4