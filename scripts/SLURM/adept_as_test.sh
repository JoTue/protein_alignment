#!/bin/bash
#
#SBATCH --job-name=adept_as_test
#SBATCH --partition=gpu
#SBATCH --gpus=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 100000000
/usr/bin/time ../../../adept/build2/examples/py_examples/py_asynch_protein -q ../../data/sp_n4000_10_1000 -r ../../data/sp_n4000_10_1000 -o a
/usr/bin/time ../../../adept/build2/examples/py_examples/py_asynch_protein2 -q ../../data/sp_n4000_10_1000 -r ../../data/sp_n4000_10_1000 -o b
/usr/bin/time ../../../adept/build2/examples/py_examples/py_asynch_protein3 -q ../../data/sp_n4000_10_1000 -r ../../data/sp_n4000_10_1000 -o c