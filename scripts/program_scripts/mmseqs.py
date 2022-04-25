#!/usr/bin/env python3
"""Run MMSeqs2 on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def mmseqs(input_file, matrix, gapopen, gapextension, max_evalue, num_threads):
    name = input_file.split('/')[-1]
    # create output directory
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    try:
        os.mkdir(f"../program_out/{name}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"../program_out/{name}/mmseqs")
    except FileExistsError:
        pass

    # run mmseqs
    t1 = time.perf_counter()
    # TODO: try -s (sensitivity) and --num-iterations (PSI-BLAST like)
    subprocess.run(f"mmseqs easy-search {input_file} {input_file} ../program_out/{name}/mmseqs/{name}.mmseqs /tmp --gap-open {gapopen} --gap-extend {gapextension} --sub-mat /apps/mmseqs2/11-e1a1c/matrices/{matrix.lower()}.out -e {max_evalue} --threads {num_threads} --comp-bias-corr 1 --format-output query,target,raw -s 7.5", shell=True)
    t2 = time.perf_counter()
    with open(f"../program_out/{name}/mmseqs/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run MMSeqs2 on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run MMSeqs2 on the specified query/db file.')

    parser.add_argument("input",
        help="Input file path (used as query and db).")
    parser.add_argument("-m", "--matrix", default="BLOSUM50",
        help="Name of the substitution matrix: BLOSUM50 or BLOSUM62")
    parser.add_argument("-o", "--gapopen", type=int, default=15,
        help="Gap open penalty.")
    parser.add_argument("-e", "--gapextension", type=int, default=2,
        help="Gap extension penalty.")
    parser.add_argument("-v", "--max-evalue", type=int, default=20,
        help="Maximum e-value.")
    parser.add_argument("-t", "--num-threads", type=int, default=1,
        help="Number of CPU threads.")

    args = parser.parse_args()

    mmseqs(args.input, args.matrix, args.gapopen, args.gapextension, args.max_evalue, args.num_threads)
 
if __name__ == '__main__':
    main()
