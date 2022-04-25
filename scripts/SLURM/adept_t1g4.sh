#!/bin/bash
#
#SBATCH --job-name=adept_t1g4_c
#SBATCH --partition=gpu
#SBATCH --gpus=4
#SBATCH --cpus-per-task=1
#SBATCH --mem=1GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

/usr/bin/time ../program_scripts/adept.py data/sp_n2000_0_600
/usr/bin/time ../program_scripts/adept_as.py data/sp_n2000_0_600

/usr/bin/time ../program_scripts/adept.py data/sp_n4000_0_600
/usr/bin/time ../program_scripts/adept_as.py data/sp_n4000_0_600

/usr/bin/time ../program_scripts/adept.py data/sp_n6000_0_600
/usr/bin/time ../program_scripts/adept_as.py data/sp_n6000_0_600

/usr/bin/time ../program_scripts/adept.py data/sp_n8000_0_600
/usr/bin/time ../program_scripts/adept_as.py data/sp_n8000_0_600