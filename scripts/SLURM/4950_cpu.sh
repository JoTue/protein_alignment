#!/bin/bash
#
#SBATCH --job-name=4950_cpu
#SBATCH --cpus-per-task=12
#SBATCH --mem=10GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

/usr/bin/time ../align_database.py data/4950.fa data/4950.fa -r -p ssw_xargs swipe_xargs swipe_swlib_xargs -t 12 -s 2000 -n 4950_cpu_s2000
/usr/bin/time ../align_database.py data/4950.fa data/4950.fa -r -p ssw_xargs swipe_xargs swipe_swlib_xargs -t 12 -n 4950_cpu