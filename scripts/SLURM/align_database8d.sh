#!/bin/bash
#
#SBATCH --job-name=ad_8d
#SBATCH --partition=gpu
#SBATCH --gpus=6
#SBATCH --cpus-per-task=24
#SBATCH --mem=50GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000

# 4M
/usr/bin/time ../align_database.py data/sp_n2000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -n sp_n2000_10_500_b
#/usr/bin/time ../align_database.py data/sp_n100_10_500 data/sp_n40000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -n sp_n100_10_500.sp_n40000_10_500_b

# 8M
/usr/bin/time ../align_database.py data/sp_n2828_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -n sp_n2828_10_500_b
#/usr/bin/time ../align_database.py data/sp_n200_10_500 data/sp_n40000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -n sp_n200_10_500.sp_n40000_10_500_b

# 16M
#/usr/bin/time ../align_database.py data/sp_n4000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -n sp_n4000_10_500_b
#/usr/bin/time ../align_database.py data/sp_n400_10_500 data/sp_n40000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -n sp_n400_10_500.sp_n40000_10_500_b

# 32M
#/usr/bin/time ../align_database.py data/sp_n5656_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -n sp_n5656_10_500_b
#/usr/bin/time ../align_database.py data/sp_n800_10_500 data/sp_n40000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -n sp_n800_10_500.sp_n40000_10_500_b

# 64M
#/usr/bin/time ../align_database.py data/sp_n8000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -n sp_n8000_10_500_b
#/usr/bin/time ../align_database.py data/sp_n1600_10_500 data/sp_n40000_10_500 -r -p ssw_xargs swipe_xargs cudasw_xargs adept_as_xargs -t 24 -g 6 -n sp_n1600_10_500.sp_n40000_10_500_b
