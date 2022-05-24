#!/bin/bash
#
#SBATCH --job-name=tmpfs_test
#SBATCH --partition=gpu
#SBATCH --gpus=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000

/usr/bin/time ../align_database.py data/sp_n200_10_500 data/sp_n200_10_500 -l 1 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 4 -n tmpfs_test_po
/usr/bin/time ../align_database.py data/sp_n200_10_500 data/sp_n200_10_500 -l 1 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 4 -d $TMPDIR -n tmpfs_test_tmp
/usr/bin/time ../align_database.py data/sp_n200_10_500 data/sp_n200_10_500 -l 1 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 4 -d /dev/shm -n tmpfs_test_dev