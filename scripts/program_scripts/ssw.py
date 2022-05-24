#!/usr/bin/env python3
"""Run SSW on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def ssw(query_file, db_file, TMPDIR, name, matrix, gapopen, gapextension, min_score):
    # create output directory
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    try:
        os.mkdir(f"{TMPDIR}/{name}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"{TMPDIR}/{name}/ssw")
    except FileExistsError:
        pass

    # run ssw
    t1 = time.perf_counter()
    subprocess.run(f"../ssw/Complete-Striped-Smith-Waterman-Library/src/pyssw.py -a {matrix} -o {gapopen} -e {gapextension} -f {min_score} -p -l ../ssw/Complete-Striped-Smith-Waterman-Library/src/libssw.so {db_file} {query_file} > {TMPDIR}/{name}/ssw/{name}.ssw", shell=True)
    t2 = time.perf_counter()
    with open(f"{TMPDIR}/{name}/ssw/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run SSW on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run SSW on the specified query/db file.')

    parser.add_argument("input", nargs="+",
        help="File paths of query and database files (space-separated). If only one file path is given, it will be used as query and database.")
    parser.add_argument("-d", "--tmp-dir", default=f"{os.path.dirname(os.path.dirname(sys.path[0]))}/program_out",
        help="Directory path used as temporary directory to read in files and write output.")
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

    ssw(query_file, db_file, args.tmp_dir, name, args.matrix, args.gapopen, args.gapextension, args.min_score)
 
if __name__ == '__main__':
    main()

# matrix: default BLOSUM50, error for other matrices (-a)