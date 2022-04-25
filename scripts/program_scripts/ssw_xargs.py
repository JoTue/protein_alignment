#!/usr/bin/env python3
"""Run SSW on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def ssw_xargs(input_file, matrix, gapopen, gapextension, num_threads, min_score):
    name = input_file.split('/')[-1]
    # create output directory
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    try:
        os.mkdir(f"../program_out/{name}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"../program_out/{name}/ssw_xargs")
    except FileExistsError:
        pass

    chunk_n = len(os.listdir(f"{os.path.dirname(input_file)}/qchunks"))//4
    print(f"{chunk_n=}")
    threads_n = num_threads

    # run ssw
    t1 = time.perf_counter()
    # FIXME: ignore matrix argument for now (error with -a option), default: BLOSUM50
    # simap command: seq $QCHUNKS | xargs -I{} --max-procs=$NTHREADS bash -c "../bin/swipe_swlib -M BLOSUM50 -G 13 -E 2 -c 55 -B 75 -i $QTMPDIR/q.{} -d $DTMPDIR/d -m 88 -s2 -b $nseq -v $nseq -o $QTMPDIR/t.{} && mv $QTMPDIR/t.{} $QTMPDIR/r.{}"
    subprocess.run(f"seq {chunk_n} | xargs -I[] --max-procs={threads_n} bash -c 'date; ../ssw/Complete-Striped-Smith-Waterman-Library/src/pyssw.py -o {gapopen} -e {gapextension} -f {min_score} -p -l ../ssw/Complete-Striped-Smith-Waterman-Library/src/libssw.so {input_file} {os.path.dirname(input_file)}/qchunks/q_[] > ../program_out/{name}/ssw_xargs/[].ssw_xargs'", shell=True)
    t2 = time.perf_counter()
    with open(f"../program_out/{name}/ssw_xargs/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run ssw_xargs on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run ssw_xargs on the specified query/db file.')

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

    args = parser.parse_args()

    ssw_xargs(args.input, args.matrix, args.gapopen, args.gapextension, args.num_threads, args.min_score)
 
if __name__ == '__main__':
    main()

# matrix: default BLOSUM50, error for other matrices (-a)