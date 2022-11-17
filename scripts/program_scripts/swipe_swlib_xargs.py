#!/usr/bin/env python3
"""Run swipe_swlib on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def swipe_swlib_xargs(query_file, db_file, TMPDIR, name, matrix, gapopen, gapextension, num_threads, min_score, min_score2, chunk_s):
    # create output directory
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    try:
        os.mkdir(f"{TMPDIR}/{name}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"{TMPDIR}/{name}/swipe_swlib_xargs")
    except FileExistsError:
        pass

    if chunk_s:
        chunk_name = "qchunks"
    else:
        chunk_name = "qchunks_cpu"

    chunk_n = len(os.listdir(f"{os.path.dirname(query_file)}/{chunk_name}"))
    print(f"{chunk_n=}")
    threads_n = num_threads
    seq_n = int(subprocess.check_output(f"grep -c '^>' {db_file}", shell=True))
    
    # bash: export LD_LIBRARY_PATH=/scratch/cube/tuechler/simap2/string2020/clip/lib:$LD_LIBRARY_PATH

    # run swipe_swlib
    t1 = time.perf_counter()
    # simap command: seq $QCHUNKS | xargs -I{} --max-procs=$NTHREADS bash -c "../bin/swipe_swlib -M BLOSUM50 -G 13 -E 2 -c 55 -B 75 -i $QTMPDIR/q.{} -d $DTMPDIR/d -m 88 -s2 -b $nseq -v $nseq -o $QTMPDIR/t.{} && mv $QTMPDIR/t.{} $QTMPDIR/r.{}"
    # swipe_swlib: -e not needed; -s2 ?

    subprocess.run(f"seq {chunk_n} | xargs -I[] --max-procs={threads_n} bash -c 'echo start []; date; uptime; ../simap2/string2020/clip/bin/swipe_swlib -i {os.path.dirname(query_file)}/{chunk_name}/q_[] -d {db_file} -G {gapopen-gapextension} -E {gapextension} -M {matrix} -b {seq_n} -v {seq_n} -c {min_score} -B {min_score2} -s2 -m 88 -o {TMPDIR}/{name}/swipe_swlib_xargs/[].swipe_swlib_xargs ; echo end []; date; uptime'", shell=True)
    # subprocess.run(f"seq {chunk_n} | xargs -I[] --max-procs={threads_n} bash -c 'echo start []; date; uptime; ../swipe/swipe -i {os.path.dirname(query_file)}/{chunk_name}/q_[] -d {db_file} -G {gapopen-gapextension} -E {gapextension} -M {matrix} -b {seq_n} -v {seq_n} -c {min_score} -B {min_score2} -s2 -m 88 -o {TMPDIR}/{name}/swipe_swlib_xargs/[].swipe_swlib_xargs ; echo end []; date; uptime'", shell=True)
    t2 = time.perf_counter()
    with open(f"{TMPDIR}/{name}/swipe_swlib_xargs/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run swipe_swlib on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run swipe_swlib on the specified query/db file.')

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
    parser.add_argument("-B", "--min-score2", type=int, default=75,
        help="Minimimum score cutoff of stage 2 of swipe_swlib.")
    parser.add_argument("-t", "--num-threads", type=int, default=1,
        help="Number of CPU threads.")
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

    swipe_swlib_xargs(query_file, db_file, args.tmp_dir, name, args.matrix, args.gapopen, args.gapextension, args.num_threads, args.min_score, args.min_score2, args.chunksize)
 
if __name__ == '__main__':
    main()
