#!/usr/bin/env python3
"""Run dedal on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def dedal(query_file, db_file, name, matrix, gapopen, gapextension):
    # create output directory
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    try:
        os.mkdir(f"../program_out/{name}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"../program_out/{name}/dedal")
    except FileExistsError:
        pass

    # run dedal
    subprocess.run("module load dedal", shell=True)
    t1 = time.perf_counter()
    subprocess.run(f"/scratch/cube/tuechler/dedal_test/dedal_program_script.py {query_file}", shell=True)
    t2 = time.perf_counter()
    subprocess.run("module unload dedal", shell=True) # probably not required...
    with open(f"../program_out/{name}/dedal/time.txt", "w") as f:
        f.write(f"{t2 - t1}")


def main():
    """ 
    Run dedal on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run dedal on the specified query/db file.')

    parser.add_argument("input", nargs="+",
        help="File paths of query and database files (space-separated). If only one file path is given, it will be used as query and database.")
    parser.add_argument("-n", "--name", default=None,
        help="Name of output directory. ")  
    parser.add_argument("-m", "--matrix", default="BLOSUM50",
        help="Name of the substitution matrix: BLOSUM50 or BLOSUM62")
    parser.add_argument("-o", "--gapopen", type=int, default=15,
        help="Gap open penalty.")
    parser.add_argument("-e", "--gapextension", type=int, default=2,
        help="Gap extension penalty.")

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

    dedal(query_file, db_file, name, args.matrix, args.gapopen, args.gapextension)
 
if __name__ == '__main__':
    main()
