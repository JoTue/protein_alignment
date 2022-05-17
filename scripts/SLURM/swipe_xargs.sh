#!/bin/bash
#
#SBATCH --job-name=swipe_xargs
#SBATCH --cpus-per-task=24
#SBATCH --mem=1GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000

# /usr/bin/time ../align_database.py data/sp_n2000_0_600 -r -p swipe_xargs ssw_xargs -t 1
# echo -t 1

/usr/bin/time ../align_database.py data/sp_n2000_0_600 -r -p swipe_xargs ssw_xargs -t 4
echo -t 4

# /usr/bin/time ../align_database.py data/sp_n2000_0_600 -r -p swipe_xargs ssw_xargs -t 8
# echo -t 8

/usr/bin/time ../align_database.py data/sp_n2000_0_600 -r -p swipe_xargs ssw_xargs -t 12
echo -t 12

# /usr/bin/time ../align_database.py data/sp_n2000_0_600 -r -p swipe_xargs ssw_xargs -t 16
# echo -t 16

# /usr/bin/time ../align_database.py data/sp_n2000_0_600 -r -p swipe_xargs ssw_xargs -t 20
# echo -t 20

/usr/bin/time ../align_database.py data/sp_n2000_0_600 -r -p swipe_xargs ssw_xargs -t 24
echo -t 24
