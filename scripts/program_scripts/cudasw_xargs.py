#!/usr/bin/env python3
"""Run CUDASW++ 3.0 on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def cudasw_xargs(input_file, matrix, gapopen, gapextension, num_threads, num_gpus, min_score):
    name = input_file.split('/')[-1]
    # create output directory
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    try:
        os.mkdir(f"../program_out/{name}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"../program_out/{name}/cudasw_xargs")
    except FileExistsError:
        pass

    chunk_n = len(os.listdir(f"{os.path.dirname(input_file)}/qchunks_gpu"))
    print(f"{chunk_n=}")
    threads_n = num_gpus

    # run CUDASW++ 3.0
    t1 = time.perf_counter()  
    # simap command: seq $QCHUNKS | xargs -I{} --max-procs=$NTHREADS bash -c "../bin/swipe_swlib -M BLOSUM50 -G 13 -E 2 -c 55 -B 75 -i $QTMPDIR/q.{} -d $DTMPDIR/d -m 88 -s2 -b $nseq -v $nseq -o $QTMPDIR/t.{} && mv $QTMPDIR/t.{} $QTMPDIR/r.{}"
    # !!! set -num_gpus BEFORE -use_single 
    subprocess.run(f"seq {chunk_n} | xargs -I[] --max-procs={threads_n} bash -c 'let \"i=[]-1\"; date; ../cudasw++v3.1.2/cudasw -qprf 1 -query {os.path.dirname(input_file)}/qchunks_gpu/q_[] -db {input_file} -mat {matrix.lower()} -gapo {gapopen-gapextension} -gape {gapextension} -num_threads 1 -num_gpus {num_gpus} -use_single $i -topscore_num 1000000 -min_score {min_score} &> ../program_out/{name}/cudasw_xargs/[].cudasw_xargs'", shell=True)
    t2 = time.perf_counter()
    with open(f"../program_out/{name}/cudasw_xargs/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run CUDASW++ 3.0 on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run CUDASW++ 3.0 on the specified query/db file.')

    parser.add_argument("input",
        help="Input file path (used as query and db).")
    parser.add_argument("-m", "--matrix", default="BLOSUM50",
        help="Name of the substitution matrix: BLOSUM50 or BLOSUM62")
    parser.add_argument("-o", "--gapopen", type=int, default=15,
        help="Gap open penalty.")
    parser.add_argument("-e", "--gapextension", type=int, default=2,
        help="Gap extension penalty.")
    parser.add_argument("-c", "--min-score", type=int, default=50,
        help="Minimimum score of alignments to show.")
    parser.add_argument("-t", "--num-threads", type=int, default=1,
        help="Number of CPU threads.")
    parser.add_argument("-g", "--num-gpus", type=int, default=1,
        help="Number of GPUs.")

    args = parser.parse_args()

    cudasw_xargs(args.input, args.matrix, args.gapopen, args.gapextension, args.num_threads, args.num_gpus, args.min_score)
 
if __name__ == '__main__':
    main()

#  -mat <string>   : specify the substitution matrix name (default blosum62)
#                 supported matrix names: blosum45, blosum50, blosum62 and blosum80
#  -num_gpus <int> : number of GPUs, (default 1)
#  -num_threads <int>      : number of CPU threads (default 4)