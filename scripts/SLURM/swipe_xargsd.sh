#!/bin/bash
#
#SBATCH --job-name=swipe_xargsd
#SBATCH --cpus-per-task=12
#SBATCH --mem=1GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000

/usr/bin/time ../align_database.py data/sp_n2000_0_600 -p swipe_xargs ssw_xargs -x swipe_xargs ssw_xargs -t 12

