#!/bin/bash
#
#SBATCH --job-name=ad_7
#SBATCH --partition=gpu
#SBATCH --gpus=6
#SBATCH --cpus-per-task=24
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000
/usr/bin/time ../align_database.py data/sp_n10000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3
/usr/bin/time ../align_database.py data/sp_n10000_10_500_b -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 24 -g 6

/usr/bin/time ../align_database.py data/sp_n10000_501_1000 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3
/usr/bin/time ../align_database.py data/sp_n10000_501_1000_b -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 24 -g 6

/usr/bin/time ../align_database.py data/sp_n10000_10_1000 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3
/usr/bin/time ../align_database.py data/sp_n10000_10_1000_b -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 24 -g 6