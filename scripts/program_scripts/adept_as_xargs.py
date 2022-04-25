#!/usr/bin/env python3
"""Run ADEPT py_asynch_protein xargs on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def adept_as_xargs(input_file, matrix, gapopen, gapextension, num_gpus):
    name = input_file.split('/')[-1]
    # create output directory
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    try:
        os.mkdir(f"../program_out/{name}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"../program_out/{name}/adept_as_xargs")
    except FileExistsError:
        pass

    chunk_n = len(os.listdir(f"{os.path.dirname(input_file)}/qchunks_gpu"))
    print(f"{chunk_n=}")
    threads_n = num_gpus

    # run adept py_asynch_protein xargs
    t1 = time.perf_counter()
    # simap command: seq $QCHUNKS | xargs -I{} --max-procs=$NTHREADS bash -c "../bin/swipe_swlib -M BLOSUM50 -G 13 -E 2 -c 55 -B 75 -i $QTMPDIR/q.{} -d $DTMPDIR/d -m 88 -s2 -b $nseq -v $nseq -o $QTMPDIR/t.{} && mv $QTMPDIR/t.{} $QTMPDIR/r.{}"
    subprocess.run(f"seq {chunk_n} | xargs -I[] --max-procs={threads_n} bash -c 'date; ../adept/build2/examples/py_examples/py_asynch_protein3 -q {os.path.dirname(input_file)}/qchunks_gpu/q_[] -r {input_file} -o ../program_out/{name}/adept_as_xargs/[].adept_as_xargs -m {matrix} --gapopen {gapopen} -e {gapextension} -g []'", shell=True)
    t2 = time.perf_counter()
    with open(f"../program_out/{name}/adept_as_xargs/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run ADEPT py_asynch_protein xargs on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run ADEPT py_asynch_protein xargs on the specified query/db file.')

    parser.add_argument("input",
        help="Input file path (used as query and db).")
    parser.add_argument("-m", "--matrix", default="BLOSUM50",
        help="Name of the substitution matrix: BLOSUM50 or BLOSUM62")
    parser.add_argument("-o", "--gapopen", type=int, default=15,
        help="Gap open penalty.")
    parser.add_argument("-e", "--gapextension", type=int, default=2,
        help="Gap extension penalty.")
    parser.add_argument("-g", "--num-gpus", type=int, default=1,
        help="Number of GPUs.")

    args = parser.parse_args()

    adept_as_xargs(args.input, args.matrix, args.gapopen, args.gapextension, args.num_gpus)
 
if __name__ == '__main__':
    main()

# Notes:
# query/ref sequences may be max 1024nt long - but shorter query/longer ref is possible (and vice versa)

# py_asynch_protein only prints results correctly up to 50000, but multigpu seems to work fine...