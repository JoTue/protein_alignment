#!/bin/bash
#
#SBATCH --job-name=ad_6b
#SBATCH --partition=gpu
#SBATCH --gpus=3
#SBATCH --cpus-per-task=12
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000
/usr/bin/time ../align_database.py data/sp_n6000_10_600_b -r -p blast mmseqs cudasw cudasw_xargs ssw ssw_xargs swipe swipe_xargs adept adept_as adept_as_xargs -t 12 -g 3