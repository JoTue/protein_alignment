#!/usr/bin/env python3
"""Run ADEPT py_asynch_protein xargs on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def adept_as_xargs(query_file, db_file, TMPDIR, name, matrix, gapopen, gapextension, min_score, num_gpus, chunk_s):
    # create output directory
    try:
        os.mkdir(f"{TMPDIR}/{name}/adept_as_xargs")
    except FileExistsError: # TODO: remove, should raise
        pass
    
    if chunk_s:
        chunk_name = "qchunks"
    else:
        chunk_name = "qchunks_gpu"

    max_query = int(subprocess.check_output(f"wc -L {query_file}", shell=True).split()[0])
    max_ref = int(subprocess.check_output(f"wc -L {db_file}", shell=True).split()[0])
    chunk_n = len(os.listdir(f"{os.path.dirname(query_file)}/{chunk_name}"))
    print(f"{chunk_n=}\n{max_query=}\n{max_ref=}")
    threads_n = num_gpus

    # run adept py_asynch_protein xargs
    t1 = time.perf_counter()
    # simap command: seq $QCHUNKS | xargs -I{} --max-procs=$NTHREADS bash -c "../bin/swipe_swlib -M BLOSUM50 -G 13 -E 2 -c 55 -B 75 -i $QTMPDIR/q.{} -d $DTMPDIR/d -m 88 -s2 -b $nseq -v $nseq -o $QTMPDIR/t.{} && mv $QTMPDIR/t.{} $QTMPDIR/r.{}"
    
    if chunk_s:
        # TODO: better GPU selection strategy
        subprocess.run(f"seq {chunk_n} | xargs -I[] --max-procs={threads_n} bash -c 'let \"i=([]-1)%{num_gpus}\"; echo start [] $i; date; uptime; nvidia-smi; ../adept/build2/examples/py_examples/py_asynch_protein5 -q {os.path.dirname(query_file)}/{chunk_name}/q_[] -r {db_file} -o {TMPDIR}/{name}/adept_as_xargs/[].adept_as_xargs -m {matrix} --gapopen {gapopen} -e {gapextension} -c {min_score} -g $i --max_query {max_query} --max_ref {max_ref} --chunk_i [] ; echo end [] $i; date; uptime; nvidia-smi'", shell=True)
    else:
        subprocess.run(f"seq {chunk_n} | xargs -I[] --max-procs={threads_n} bash -c 'let \"i=[]-1\"; echo start []; date; uptime; nvidia-smi; ../adept/build2/examples/py_examples/py_asynch_protein5 -q {os.path.dirname(query_file)}/{chunk_name}/q_[] -r {db_file} -o {TMPDIR}/{name}/adept_as_xargs/[].adept_as_xargs -m {matrix} --gapopen {gapopen} -e {gapextension} -c {min_score} -g $i --max_query {max_query} --max_ref {max_ref} --chunk_i [] ; echo end [] ; date; uptime; nvidia-smi'", shell=True)
    t2 = time.perf_counter()
    with open(f"{TMPDIR}/{name}/adept_as_xargs/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run ADEPT py_asynch_protein xargs on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run ADEPT py_asynch_protein xargs on the specified query/db file.')

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
    parser.add_argument("-c", "--min-score", type=int, default=55,
        help="Minimimum score of alignments to show.")
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

    adept_as_xargs(query_file, db_file, args.tmp_dir, name, args.matrix, args.gapopen, args.gapextension, args.min_score, args.num_gpus, args.chunksize)
 
if __name__ == '__main__':
    main()

# Notes:
# query/ref sequences may be max 1024nt long - but shorter query/longer ref is possible (and vice versa)
