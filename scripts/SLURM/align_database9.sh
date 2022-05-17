#!/bin/bash
#
#SBATCH --job-name=ad_9
#SBATCH --partition=gpu
#SBATCH --gpus=6
#SBATCH --cpus-per-task=12
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000

/usr/bin/time ../align_database.py data/sp_n200_10_500 data/sp_10_500 -r -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 12 -g 3 -n ad_9_1
/usr/bin/time ../align_database.py data/sp_n200_10_500 data/sp_10_500 -r -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 12 -g 3 -s 3000 -n ad_9_2

# /usr/bin/time ../align_database.py data/sp_n200_10_500 data/sp_10_500 -r -p adept_as_xargs -t 12 -g 3 -n ad_9_1
# /usr/bin/time ../align_database.py data/sp_n200_10_500 data/sp_10_500 -r -p adept_as_xargs -t 12 -g 3 -s 2000 -n ad_9_2