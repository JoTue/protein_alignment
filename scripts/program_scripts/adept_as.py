#!/usr/bin/env python3
"""Run ADEPT py_asynch_protein on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def adept(query_file, db_file, TMPDIR, name, matrix, gapopen, gapextension, min_score):
    # create output directory
    try:
        os.mkdir(f"{TMPDIR}/{name}/adept_as")
    except FileExistsError:
        pass

    max_query = int(subprocess.check_output(f"wc -L {query_file}", shell=True).split()[0])
    max_ref = int(subprocess.check_output(f"wc -L {db_file}", shell=True).split()[0])
    print(f"{max_query=}\n{max_ref=}")

    # run adept py_asynch_protein
    t1 = time.perf_counter()
    subprocess.run(f"../adept/build2/examples/py_examples/py_asynch_protein5 -q {query_file} -r {db_file} -o {TMPDIR}/{name}/adept_as/{name}.adept_as -m {matrix} --gapopen {gapopen} -e {gapextension}  -c {min_score} --max_query {max_query} --max_ref {max_ref}", shell=True)
    t2 = time.perf_counter()
    with open(f"{TMPDIR}/{name}/adept_as/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run ADEPT py_asynch_protein on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run ADEPT py_asynch_protein on the specified query/db file.')

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

    adept(query_file, db_file, args.tmp_dir, name, args.matrix, args.gapopen, args.gapextension, args.min_score)
 
if __name__ == '__main__':
    main()

# Notes:
# query/ref sequences may be max 1024nt long - but shorter query/longer ref is possible (and vice versa)

# py_asynch_protein only prints results correctly up to 50000, but multigpu seems to work fine...