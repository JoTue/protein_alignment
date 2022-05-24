#!/usr/bin/env python3
"""Run CUDASW++ 3.0 on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def cudasw_xargs(query_file, db_file, TMPDIR, name, matrix, gapopen, gapextension, num_threads, num_gpus, min_score, chunk_s):
    # create output directory
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    try:
        os.mkdir(f"{TMPDIR}/{name}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"{TMPDIR}/{name}/cudasw_xargs")
    except FileExistsError:
        pass

    if chunk_s:
        chunk_name = "qchunks"
    else:
        chunk_name = "qchunks_gpu"

    chunk_n = len(os.listdir(f"{os.path.dirname(query_file)}/{chunk_name}"))
    print(f"{chunk_n=}")
    threads_n = num_gpus

    # run CUDASW++ 3.0
    t1 = time.perf_counter()  
    # simap command: seq $QCHUNKS | xargs -I{} --max-procs=$NTHREADS bash -c "../bin/swipe_swlib -M BLOSUM50 -G 13 -E 2 -c 55 -B 75 -i $QTMPDIR/q.{} -d $DTMPDIR/d -m 88 -s2 -b $nseq -v $nseq -o $QTMPDIR/t.{} && mv $QTMPDIR/t.{} $QTMPDIR/r.{}"
    # !!! set -num_gpus BEFORE -use_single
    if chunk_s:
        # TODO: better GPU selection strategy
        subprocess.run(f"seq {chunk_n} | xargs -I[] --max-procs={threads_n} bash -c 'let \"i=([]-1)%{num_gpus}\"; echo start [] $i; date; uptime; nvidia-smi; ../cudasw++v3.1.2/cudasw -qprf 1 -query {os.path.dirname(query_file)}/{chunk_name}/q_[] -db {db_file} -mat {matrix.lower()} -gapo {gapopen-gapextension} -gape {gapextension} -num_threads 1 -num_gpus {num_gpus} -use_single $i -topscore_num 1000000 -min_score {min_score} &> {TMPDIR}/{name}/cudasw_xargs/[].cudasw_xargs ; echo end [] $i; date; uptime; nvidia-smi'", shell=True)
    else:
        subprocess.run(f"seq {chunk_n} | xargs -I[] --max-procs={threads_n} bash -c 'let \"i=[]-1\"; echo start []; date; uptime; nvidia-smi; ../cudasw++v3.1.2/cudasw -qprf 1 -query {os.path.dirname(query_file)}/{chunk_name}/q_[] -db {db_file} -mat {matrix.lower()} -gapo {gapopen-gapextension} -gape {gapextension} -num_threads 1 -num_gpus {num_gpus} -use_single $i -topscore_num 1000000 -min_score {min_score} &> {TMPDIR}/{name}/cudasw_xargs/[].cudasw_xargs ; echo end []; date; uptime; nvidia-smi'", shell=True)
    t2 = time.perf_counter()
    with open(f"{TMPDIR}/{name}/cudasw_xargs/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run CUDASW++ 3.0 on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run CUDASW++ 3.0 on the specified query/db file.')

    parser.add_argument("input", nargs="+",
        help="File paths of query and database files (space-separated). If only one file path is given, it will be used as query and database.")
    parser.add_argument("-d", "--tmp-dir", default=f"{os.path.dirname(os.path.dirname(sys.path[0]))}/program_out",
        help="Directory path used as temporary directory to read in files and write output.")
    parser.add_argument("-n", "--name", default=None,
        help="Name of output directory. ")  
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
    parser.add_argument("-s", "--chunksize", type=int, default=0,
        help="Maximal number of residues for each chunk used for xargs-scripts. If 0 (default) the chunknumber is equal to the thread/GPU number.")

    args = parser.parse_args()

    # parsing input file paths
    if len(args.input) == 1:
        query_file = args.input[0]
        db_file = args.input[0]
    elif len(args.input) == 2:
        query_file = args.input[0]
        db_file = args.input[1]
    else:
        raise Exception("Specify 1 or 2 file paths.")

    name = args.name
    if name == None:
        name = f"{query_file.split('/')[-1]}.{db_file.split('/')[-1]}"

    cudasw_xargs(query_file, db_file, args.tmp_dir, name, args.matrix, args.gapopen, args.gapextension, args.num_threads, args.num_gpus, args.min_score, args.chunksize)
 
if __name__ == '__main__':
    main()

#  -mat <string>   : specify the substitution matrix name (default blosum62)
#                 supported matrix names: blosum45, blosum50, blosum62 and blosum80
#  -num_gpus <int> : number of GPUs, (default 1)
#  -num_threads <int>      : number of CPU threads (default 4)