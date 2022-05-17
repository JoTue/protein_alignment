#!/bin/bash
#
#SBATCH --job-name=swipe_xargsc
#SBATCH --cpus-per-task=16
#SBATCH --mem=1GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000


/usr/bin/time ../align_database.py data/sp_n50_10_500 data/sp_10_1000 -r -p swipe_xargs ssw_xargs -t 8
echo -t 8

/usr/bin/time ../align_database.py data/sp_n50_10_500 data/sp_10_1000 -r -p swipe_xargs ssw_xargs -t 16
echo -t 16

/usr/bin/time ../align_database.py data/sp_n100_10_500 data/sp_10_1000 -r -p swipe_xargs ssw_xargs -t 8
echo -t 8

/usr/bin/time ../align_database.py data/sp_n100_10_500 data/sp_10_1000 -r -p swipe_xargs ssw_xargs -t 16
echo -t 16
