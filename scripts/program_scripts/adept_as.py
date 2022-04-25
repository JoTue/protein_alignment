#!/usr/bin/env python3
"""Run ADEPT py_asynch_protein on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def adept(input_file, matrix, gapopen, gapextension):
    name = input_file.split('/')[-1]
    # create output directory
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    try:
        os.mkdir(f"../program_out/{name}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"../program_out/{name}/adept_as")
    except FileExistsError:
        pass

    # run adept py_asynch_protein
    t1 = time.perf_counter()
    subprocess.run(f"../adept/build2/examples/py_examples/py_asynch_protein3 -q {input_file} -r {input_file} -o  ../program_out/{name}/adept_as/{name}.adept_as -m {matrix} --gapopen {gapopen} -e {gapextension}", shell=True)
    t2 = time.perf_counter()
    with open(f"../program_out/{name}/adept_as/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run ADEPT py_asynch_protein on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run ADEPT py_asynch_protein on the specified query/db file.')

    parser.add_argument("input",
        help="Input file path (used as query and db).")
    parser.add_argument("-m", "--matrix", default="BLOSUM50",
        help="Name of the substitution matrix: BLOSUM50 or BLOSUM62")
    parser.add_argument("-o", "--gapopen", type=int, default=15,
        help="Gap open penalty.")
    parser.add_argument("-e", "--gapextension", type=int, default=2,
        help="Gap extension penalty.")

    args = parser.parse_args()

    adept(args.input, args.matrix, args.gapopen, args.gapextension)
 
if __name__ == '__main__':
    main()

# Notes:
# query/ref sequences may be max 1024nt long - but shorter query/longer ref is possible (and vice versa)

# py_asynch_protein only prints results correctly up to 50000, but multigpu seems to work fine...