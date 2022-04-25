#!/bin/bash
#
#SBATCH --job-name=ad_5b
#SBATCH --partition=gpu
#SBATCH --gpus=6
#SBATCH --cpus-per-task=12
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000
/usr/bin/time ../align_database.py data/sp_n4000_10_1000_b -r -p blast mmseqs cudasw ssw ssw_xargs swipe swipe_xargs adept adept_as adept_as_xargs -t 24 -g 6