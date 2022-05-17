#!/bin/bash
#
#SBATCH --job-name=ad_10d
#SBATCH --partition=gpu
#SBATCH --gpus=6
#SBATCH --cpus-per-task=24
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000

/usr/bin/time ../align_database.py data/sp_n300_10_1000 data/sp_10_1000 -l 0 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -s 3000 -n ad_10d_24_6
/usr/bin/time ../align_database.py data/sp_n300_10_1000 data/sp_10_1000 -l 0 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 12 -g 3 -s 3000 -n ad_10d_12_3