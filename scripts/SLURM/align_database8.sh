#!/bin/bash
#
#SBATCH --job-name=ad_8
#SBATCH --partition=gpu
#SBATCH --gpus=3
#SBATCH --cpus-per-task=12
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000
/usr/bin/time ../align_database.py data/sp_n2000_10_500 -r -p blast mmseqs cudasw cudasw_xargs ssw ssw_xargs swipe swipe_xargs adept adept_as adept_as_xargs -t 12 -g 3

/usr/bin/time ../align_database.py data/sp_n100_10_500 data/sp_n40000_10_500 -r -p blast mmseqs cudasw cudasw_xargs ssw ssw_xargs swipe swipe_xargs adept adept_as adept_as_xargs -t 12 -g 3

/usr/bin/time ../align_database.py data/sp_n40000_10_500 data/sp_n100_10_500 -r -p blast mmseqs cudasw cudasw_xargs ssw ssw_xargs swipe swipe_xargs adept adept_as adept_as_xargs -t 12 -g 3
