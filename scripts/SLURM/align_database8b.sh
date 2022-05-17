#!/bin/bash
#
#SBATCH --job-name=ad_8b
#SBATCH --partition=gpu
#SBATCH --gpus=3
#SBATCH --cpus-per-task=12
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000
/usr/bin/time ../align_database.py data/sp_n2828_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3

/usr/bin/time ../align_database.py data/sp_n200_10_500 data/sp_n40000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3
