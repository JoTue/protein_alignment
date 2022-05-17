#!/bin/bash
#
#SBATCH --job-name=ad_8e
#SBATCH --partition=gpu
#SBATCH --gpus=3
#SBATCH --cpus-per-task=12
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000

# fixed query size, different database sizes:

/usr/bin/time ../align_database.py data/sp_n1000_10_500 data/sp_n1000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3
/usr/bin/time ../align_database.py data/sp_n1000_10_500 data/sp_n4000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3
/usr/bin/time ../align_database.py data/sp_n1000_10_500 data/sp_n16000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3
/usr/bin/time ../align_database.py data/sp_n1000_10_500 data/sp_n64000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3
/usr/bin/time ../align_database.py data/sp_n1000_10_500 data/sp_n256000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3
