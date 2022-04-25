#!/bin/bash
#
#SBATCH --job-name=sp_n4000_b
#SBATCH --partition=gpu
#SBATCH --gpus=4
#SBATCH --cpus-per-task=12
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000
/usr/bin/time ../align_database.py data/sp_n4000_10_500_b -r -t 12 -g 4 -p blast mmseqs ssw swipe cudasw adept adept_as -x ssw swipe cudasw adept adept_as
/usr/bin/time ../align_database.py data/sp_n4000_10_1000_b -r -t 12 -g 4 -p blast mmseqs ssw swipe cudasw adept adept_as -x ssw swipe cudasw adept adept_as
/usr/bin/time ../align_database.py data/sp_n4000_501_1000_b -r -t 12 -g 4 -p blast mmseqs ssw swipe cudasw adept adept_as -x ssw swipe cudasw adept adept_as