#!/bin/bash
#
#SBATCH --job-name=ad_9b
#SBATCH --partition=gpu
#SBATCH --gpus=6
#SBATCH --cpus-per-task=12
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000

/usr/bin/time ../align_database.py data/sp_n300_10_1000 data/sp_10_1000 -r -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 12 -g 3 -n ad_9b_1
/usr/bin/time ../align_database.py data/sp_n300_10_1000 data/sp_10_1000 -r -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 12 -g 3 -s 2000 -n ad_9b_2