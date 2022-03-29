#!/usr/bin/env python3
"""Run SWIPE on the specified query/db file"""

import subprocess
import os
import time
import argparse

# TODO: -v/-b options (show more hits)

def swipe(input_file, matrix, gapopen, gapextension):
    name = input_file.split('/')[-1]
    # create output directory
    try:
        os.mkdir(f"program_out/{name}/swipe")
    except FileExistsError:
        pass

    # run swipe
    t1 = time.perf_counter()
    subprocess.run(f"swipe -i {input_file} -d {input_file} -G {gapopen-gapextension} -E {gapextension} -M {matrix} -e 1000000000 -b 1000000000 -v 1000000000 -c 0 -a 1 > program_out/{name}/swipe/{name}.swipe", shell=True)
    t2 = time.perf_counter()
    with open(f"program_out/{name}/swipe/time.txt", "w") as f:
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

    args = parser.parse_args()

    swipe(args.input, args.matrix, args.gapopen, args.gapextension)
 
if __name__ == '__main__':
    main()

# Matrix: -M BLOSUM50/BLOSUM62
# -a, --num_threads=NUM      number of threads to use [1-256]