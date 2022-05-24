#!/bin/bash
#
#SBATCH --job-name=adept_test
#SBATCH --partition=gpu
#SBATCH --gpus=6
#SBATCH --cpus-per-task=24
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000

/usr/bin/time ../align_database.py data/sp_n500_10_500 data/sp_n256000_10_500 -l 1 -p adept_as_xargs -t 24 -g 6 -s 3000 -n adept_test_1

/usr/bin/time ../align_database.py data/sp_n500_10_500 data/sp_n256000_10_500 -l 1 -p adept_as_xargs -t 24 -g 6 -d $TMPDIR -n adept_test_2

/usr/bin/time ../align_database.py data/sp_n500_10_500 data/sp_n256000_10_500 -l 1 -p adept_as_xargs -t 24 -g 6 -n adept_test_3
