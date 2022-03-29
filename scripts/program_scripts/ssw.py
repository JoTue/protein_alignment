#!/usr/bin/env python3
"""Run SSW on the specified query/db file"""

import subprocess
import os
import time
import argparse

def ssw(input_file, matrix, gapopen, gapextension):
    name = input_file.split('/')[-1]
    # create output directory
    try:
        os.mkdir(f"program_out/{name}/ssw")
    except FileExistsError:
        pass

    # run ssw
    t1 = time.perf_counter()
    # FIXME: ignore matrix argument for now (error with -a option), default: BLOSUM50
    subprocess.run(f"../ssw/Complete-Striped-Smith-Waterman-Library/src/pyssw.py -o {gapopen} -e {gapextension} -p -l ../ssw/Complete-Striped-Smith-Waterman-Library/src/libssw.so {input_file} {input_file} > program_out/{name}/ssw/{name}.ssw", shell=True)
    t2 = time.perf_counter()
    with open(f"program_out/{name}/ssw/time.txt", "w") as f:
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

    args = parser.parse_args()

    ssw(args.input, args.matrix, args.gapopen, args.gapextension)
 
if __name__ == '__main__':
    main()

# matrix: default BLOSUM50, error for other matrices (-a)