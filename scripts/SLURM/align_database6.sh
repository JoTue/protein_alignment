#!/bin/bash
#
#SBATCH --job-name=ad_6
#SBATCH --partition=gpu
#SBATCH --gpus=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000
/usr/bin/time ../align_database.py data/sp_n6000_10_600 -r -p blast mmseqs cudasw cudasw_xargs ssw ssw_xargs swipe swipe_xargs adept adept_as adept_as_xargs -t 1 -g 1