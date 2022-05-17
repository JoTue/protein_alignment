#!/usr/bin/env python3
"""Run SWIPE on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def swipe(query_file, db_file, name, matrix, gapopen, gapextension, num_threads, min_score):
    # create output directory
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    try:
        os.mkdir(f"../program_out/{name}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"../program_out/{name}/swipe")
    except FileExistsError:
        pass

    seq_n = int(subprocess.check_output(f"grep -c '^>' {db_file}", shell=True))

    # run swipe
    t1 = time.perf_counter()
    subprocess.run(f"swipe -i {query_file} -d {db_file} -G {gapopen-gapextension} -E {gapextension} -M /apps/emboss/6.6.0/emboss/data/E{matrix} -a {num_threads} -e 1000000 -b {seq_n} -v {seq_n} -c {min_score} > ../program_out/{name}/swipe/{name}.swipe", shell=True)
    t2 = time.perf_counter()
    with open(f"../program_out/{name}/swipe/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run SWIPE on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run SWIPE on the specified query/db file.')

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
    parser.add_argument("-c", "--min-score", type=int, default=50,
        help="Minimimum score of alignments to show.")
    parser.add_argument("-t", "--num-threads", type=int, default=1,
        help="Number of CPU threads.")

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

    swipe(query_file, db_file, name, args.matrix, args.gapopen, args.gapextension, args.num_threads, args.min_score)
 
if __name__ == '__main__':
    main()

# Matrix: -M BLOSUM50/BLOSUM62
# -a, --num_threads=NUM      number of threads to use [1-256]