#!/bin/bash
#
#SBATCH --job-name=ad_11
#SBATCH --partition=gpu
#SBATCH --gpus=6
#SBATCH --cpus-per-task=24
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000

# compare different tmp-directories, test if scale up to 24/6
# -> output: check CPU usage, check end time difference between chunks
# further scripts: test on quadratic matrix, test with chunksize parameter

/usr/bin/time ../align_database.py data/sp_n500_20_500 data/sp_n256000_20_500 -l 1 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -n ad_11_po_246
/usr/bin/time ../align_database.py data/sp_n500_20_500 data/sp_n256000_20_500 -l 1 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 12 -g 3 -n ad_11_po_123

/usr/bin/time ../align_database.py data/sp_n500_20_500 data/sp_n256000_20_500 -l 1 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -d $TMPDIR -n ad_11_tmp_246
/usr/bin/time ../align_database.py data/sp_n500_20_500 data/sp_n256000_20_500 -l 1 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 12 -g 3 -d $TMPDIR -n ad_11_tmp_123

/usr/bin/time ../align_database.py data/sp_n500_20_500 data/sp_n256000_20_500 -l 1 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -d /dev/shm -n ad_11_dev_246
/usr/bin/time ../align_database.py data/sp_n500_20_500 data/sp_n256000_20_500 -l 1 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 12 -g 3 -d /dev/shm -n ad_11_dev_123