#!/bin/bash
#
#SBATCH --job-name=4950_0_1000
#SBATCH --partition=gpu
#SBATCH --gpus=6
#SBATCH --cpus-per-task=12
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000

/usr/bin/time ../align_database.py data/4950_0_1000.fa data/4950_0_1000.fa -r -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 12 -g 3 -s 2000 -n 4950_0_1000_s2000
/usr/bin/time ../align_database.py data/4950_0_1000.fa data/4950_0_1000.fa -r -p ssw_xargs swipe_xargs swipe_swlib_xargs cudasw_xargs adept_as_xargs -t 12 -g 3 -n 4950_0_1000
