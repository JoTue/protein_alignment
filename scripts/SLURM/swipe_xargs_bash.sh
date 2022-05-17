#!/bin/bash
#
#SBATCH --job-name=swipe_xargs_bash
#SBATCH --cpus-per-task=8
#SBATCH --mem=1GB
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out

ulimit -v 300000000

/usr/bin/time bash -c "seq 8 | xargs -I[] --max-procs=8 bash -c 'echo start []; date; swipe -i /scratch/cube/tuechler/program_out/sp_n2000_0_600/data/qchunks/q_[] -d /scratch/cube/tuechler/program_out/sp_n2000_0_600/data/sp_n2000_0_600 -G 13 -E 2 -M /apps/emboss/6.6.0/emboss/data/EBLOSUM50 -e 1000000 -b 2000 -v 2000 -c 50 > /scratch/cube/tuechler/swipe_test/[].swipe_xargs ; echo end []; date'"