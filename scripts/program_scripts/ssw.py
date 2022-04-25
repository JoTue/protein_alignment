#!/usr/bin/env python3
"""Run SSW on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def ssw(input_file, matrix, gapopen, gapextension, min_score):
    name = input_file.split('/')[-1]
    # create output directory
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    try:
        os.mkdir(f"../program_out/{name}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"../program_out/{name}/ssw")
    except FileExistsError:
        pass

    # run ssw
    t1 = time.perf_counter()
    # FIXME: ignore matrix argument for now (error with -a option), default: BLOSUM50
    subprocess.run(f"../ssw/Complete-Striped-Smith-Waterman-Library/src/pyssw.py -o {gapopen} -e {gapextension} -f {min_score} -p -l ../ssw/Complete-Striped-Smith-Waterman-Library/src/libssw.so {input_file} {input_file} > ../program_out/{name}/ssw/{name}.ssw", shell=True)
    t2 = time.perf_counter()
    with open(f"../program_out/{name}/ssw/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run SSW on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run SSW on the specified query/db file.')

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

    args = parser.parse_args()

    ssw(args.input, args.matrix, args.gapopen, args.gapextension, args.min_score)
 
if __name__ == '__main__':
    main()

# matrix: default BLOSUM50, error for other matrices (-a)