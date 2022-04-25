#!/bin/bash
#
#SBATCH --job-name=adept_t1g2
#SBATCH --partition=gpu
#SBATCH --gpus=2
#SBATCH --cpus-per-task=1
#SBATCH --mem=1GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

/usr/bin/time ../program_scripts/adept.py data/sp_n10_b
/usr/bin/time ../program_scripts/adept_as.py data/sp_n10_b

/usr/bin/time ../program_scripts/adept.py data/sp_n300_0_600_b
/usr/bin/time ../program_scripts/adept_as.py data/sp_n300_0_600_b

/usr/bin/time ../program_scripts/adept.py data/sp_n10000_0_600
/usr/bin/time ../program_scripts/adept_as.py data/sp_n10000_0_600