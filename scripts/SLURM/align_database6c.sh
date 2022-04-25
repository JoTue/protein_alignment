#!/bin/bash
#
#SBATCH --job-name=ad_6c
#SBATCH --partition=gpu
#SBATCH --gpus=6
#SBATCH --cpus-per-task=24
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000
/usr/bin/time ../align_database.py data/sp_n6000_10_600_c -r -p blast mmseqs cudasw cudasw_xargs ssw ssw_xargs swipe swipe_xargs adept adept_as adept_as_xargs -t 24 -g 6