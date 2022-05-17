#!/bin/bash
#
#SBATCH --job-name=swipe_xargsb
#SBATCH --cpus-per-task=16
#SBATCH --mem=1GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000

/usr/bin/time ../align_database.py data/sp_n5_10_500 data/sp_10_500 -r -p swipe_xargs ssw_xargs -t 1
echo -t 1

/usr/bin/time ../align_database.py data/sp_n5_10_500 data/sp_10_500 -r -p swipe_xargs ssw_xargs -t 8
echo -t 8

/usr/bin/time ../align_database.py data/sp_n5_10_500 data/sp_10_500 -r -p swipe_xargs ssw_xargs -t 16
echo -t 16

/usr/bin/time ../align_database.py data/sp_n5_10_500 data/sp_n64000_10_500 -r -p swipe_xargs ssw_xargs -t 1
echo -t 1

/usr/bin/time ../align_database.py data/sp_n5_10_500 data/sp_n64000_10_500 -r -p swipe_xargs ssw_xargs -t 8
echo -t 8

/usr/bin/time ../align_database.py data/sp_n5_10_500 data/sp_n64000_10_500 -r -p swipe_xargs ssw_xargs -t 16
echo -t 16