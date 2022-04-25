#!/usr/bin/env python3
"""Run SWIPE on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def swipe_xargs(input_file, matrix, gapopen, gapextension, num_threads, min_score):
    name = input_file.split('/')[-1]
    # create output directory
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    try:
        os.mkdir(f"../program_out/{name}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"../program_out/{name}/swipe_xargs")
    except FileExistsError:
        pass

    chunk_n = len(os.listdir(f"{os.path.dirname(input_file)}/qchunks"))//4
    print(f"{chunk_n=}")
    threads_n = num_threads

    # run swipe
    t1 = time.perf_counter()
    # simap command: seq $QCHUNKS | xargs -I{} --max-procs=$NTHREADS bash -c "../bin/swipe_swlib -M BLOSUM50 -G 13 -E 2 -c 55 -B 75 -i $QTMPDIR/q.{} -d $DTMPDIR/d -m 88 -s2 -b $nseq -v $nseq -o $QTMPDIR/t.{} && mv $QTMPDIR/t.{} $QTMPDIR/r.{}"
    subprocess.run(f"seq {chunk_n} | xargs -I[] --max-procs={threads_n} bash -c 'date; swipe -i {os.path.dirname(input_file)}/qchunks/q_[] -d {input_file} -G {gapopen-gapextension} -E {gapextension} -M /apps/emboss/6.6.0/emboss/data/E{matrix} -e 1000000000 -b 1000000000 -v 1000000000 -c {min_score} > ../program_out/{name}/swipe_xargs/[].swipe_xargs'", shell=True)
    t2 = time.perf_counter()
    with open(f"../program_out/{name}/swipe_xargs/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run SWIPE on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run SWIPE on the specified query/db file.')

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

    swipe_xargs(args.input, args.matrix, args.gapopen, args.gapextension, args.num_threads, args.min_score)
 
if __name__ == '__main__':
    main()

# Matrix: -M BLOSUM50/BLOSUM62
# -a, --num_threads=NUM      number of threads to use [1-256]