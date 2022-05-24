#!/bin/bash
#
#SBATCH --job-name=ad_11b
#SBATCH --partition=gpu
#SBATCH --gpus=6
#SBATCH --cpus-per-task=24
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000

# bigger datasets as in ad_11, with cpu_usage plot, new (more even) chunk-splitting method

/usr/bin/time ../align_database.py data/sp_n1000_20_1000 data/sp_n256000_20_1000 -l 1 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -n ad_11b_po_246
/usr/bin/time ../align_database.py data/sp_n1000_20_1000 data/sp_n256000_20_1000 -l 1 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 12 -g 3 -n ad_11b_po_123

/usr/bin/time ../align_database.py data/sp_n1000_20_1000 data/sp_n256000_20_1000 -l 1 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -d $TMPDIR -n ad_11b_tmp_246
/usr/bin/time ../align_database.py data/sp_n1000_20_1000 data/sp_n256000_20_1000 -l 1 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 12 -g 3 -d $TMPDIR -n ad_11b_tmp_123

/usr/bin/time ../align_database.py data/sp_n1000_20_1000 data/sp_n256000_20_1000 -l 1 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -d /dev/shm -n ad_11b_dev_246
/usr/bin/time ../align_database.py data/sp_n1000_20_1000 data/sp_n256000_20_1000 -l 1 -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 12 -g 3 -d /dev/shm -n ad_11b_dev_123