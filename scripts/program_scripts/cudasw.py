#!/usr/bin/env python3
"""Run CUDASW++ 3.0 on the specified query/db file"""

import subprocess
import os
import time
import argparse

def cudasw(input_file, matrix, gapopen, gapextension):
    name = input_file.split('/')[-1]
    # create output directory
    try:
        os.mkdir(f"program_out/{name}/cudasw")
    except FileExistsError:
        pass

    # run CUDASW++ 3.0
    t1 = time.perf_counter()
    
    # -qprf 0 fails (for larger files?)
    subprocess.run(f"../cudasw++v3.1.2/cudasw -qprf 1 -query {input_file} -db {input_file} -mat {matrix.lower()} -gapo {gapopen-gapextension} -gape {gapextension} -topscore_num 1000000 -min_score 0 -num_gpus 1 -num_threads 1 &> program_out/{name}/cudasw/{name}.cudasw", shell=True)
    
    # TODO: experiment which (file sizes)/sequence lengths (500?) are ok, try out -qrpf 0/1
    # or: split query file in separate input files
    # for query in os.scandir(f"{input_file}_separate"):
    #     subprocess.run(f"../cudasw++v3.1.2/cudasw -qprf 1 -query {query.path} -db {input_file} -mat {matrix.lower()} -gapo {gapopen-gapextension} -gape {gapextension} -topscore_num 1000000 -min_score 0 -num_gpus 1 -num_threads 4 &> program_out/{name}/cudasw/{query.name}.cudasw", shell=True)

    t2 = time.perf_counter()
    with open(f"program_out/{name}/cudasw/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run CUDASW++ 3.0 on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run CUDASW++ 3.0 on the specified query/db file.')

    parser.add_argument("input",
        help="Input file path (used as query and db).")
    parser.add_argument("-m", "--matrix", default="BLOSUM50",
        help="Name of the substitution matrix: BLOSUM50 or BLOSUM62")
    parser.add_argument("-o", "--gapopen", type=int, default=15,
        help="Gap open penalty.")
    parser.add_argument("-e", "--gapextension", type=int, default=2,
        help="Gap extension penalty.")

    args = parser.parse_args()

    cudasw(args.input, args.matrix, args.gapopen, args.gapextension)
 
if __name__ == '__main__':
    main()

#  -mat <string>   : specify the substitution matrix name (default blosum62)
#                 supported matrix names: blosum45, blosum50, blosum62 and blosum80
#  -num_gpus <int> : number of GPUs, (default 1)
#  -num_threads <int>      : number of CPU threads (default 4)