#!/bin/bash
#
#SBATCH --job-name=ad_7c
#SBATCH --partition=gpu
#SBATCH --gpus=6
#SBATCH --cpus-per-task=24
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000
/usr/bin/time ../program_scripts/swipe_xargs.py ../program_out/sp_n10000_10_1000_c/data/sp_n10000_10_1000_c -t 24