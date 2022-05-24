#!/usr/bin/env python3
"""Run CUDASW++ 3.0 on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def cudasw(query_file, db_file, TMPDIR, name, matrix, gapopen, gapextension, num_threads, num_gpus, min_score):
    # create output directory
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    try:
        os.mkdir(f"{TMPDIR}/{name}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"{TMPDIR}/{name}/cudasw")
    except FileExistsError:
        pass

    # run CUDASW++ 3.0
    t1 = time.perf_counter()
    
    # -qprf 0 fails (for larger files?)
    subprocess.run(f"../cudasw++v3.1.2/cudasw -qprf 1 -query {query_file} -db {db_file} -mat {matrix.lower()} -gapo {gapopen-gapextension} -gape {gapextension} -num_threads {num_threads} -num_gpus {num_gpus} -topscore_num 1000000 -min_score {min_score} &> {TMPDIR}/{name}/cudasw/{name}.cudasw", shell=True)

    # TODO: experiment which (file sizes)/sequence lengths (500?) are ok, try out -qrpf 0/1
    # or: split query file in separate input files
    # for query in os.scandir(f"{input_file}_separate"):
    #     subprocess.run(f"../cudasw++v3.1.2/cudasw -qprf 1 -query {query.path} -db {input_file} -mat {matrix.lower()} -gapo {gapopen-gapextension} -gape {gapextension} -topscore_num 1000000 -min_score 0 -num_gpus 1 -num_threads 4 &> {TMPDIR}/{name}/cudasw/{query.name}.cudasw", shell=True)

    t2 = time.perf_counter()
    with open(f"{TMPDIR}/{name}/cudasw/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run CUDASW++ 3.0 on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run CUDASW++ 3.0 on the specified query/db file.')

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
    parser.add_argument("-t", "--num-threads", type=int, default=1,
        help="Number of CPU threads.")
    parser.add_argument("-g", "--num-gpus", type=int, default=1,
        help="Number of GPUs.")

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

    cudasw(query_file, db_file, args.tmp_dir, name, args.matrix, args.gapopen, args.gapextension, args.num_threads, args.num_gpus, args.min_score)
 
if __name__ == '__main__':
    main()

#  -mat <string>   : specify the substitution matrix name (default blosum62)
#                 supported matrix names: blosum45, blosum50, blosum62 and blosum80
#  -num_gpus <int> : number of GPUs, (default 1)
#  -num_threads <int>      : number of CPU threads (default 4)