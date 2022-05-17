#!/bin/bash
#
#SBATCH --job-name=ad_8c
#SBATCH --partition=gpu
#SBATCH --gpus=3
#SBATCH --cpus-per-task=12
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000

# # 4M
# /usr/bin/time ../align_database.py data/sp_n2000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3
# /usr/bin/time ../align_database.py data/sp_n100_10_500 data/sp_n40000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3

# # 8M
# /usr/bin/time ../align_database.py data/sp_n2828_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3
# /usr/bin/time ../align_database.py data/sp_n200_10_500 data/sp_n40000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3

# # 16M
# /usr/bin/time ../align_database.py data/sp_n4000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3
# /usr/bin/time ../align_database.py data/sp_n400_10_500 data/sp_n40000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3

# # 32M
# /usr/bin/time ../align_database.py data/sp_n5656_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3
# /usr/bin/time ../align_database.py data/sp_n800_10_500 data/sp_n40000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3

# 64M
/usr/bin/time ../align_database.py data/sp_n8000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3
/usr/bin/time ../align_database.py data/sp_n1600_10_500 data/sp_n40000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3

# 128M
/usr/bin/time ../align_database.py data/sp_n11313_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3
/usr/bin/time ../align_database.py data/sp_n3200_10_500 data/sp_n40000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 12 -g 3
