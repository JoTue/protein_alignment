#!/usr/bin/env python3
"""Run blastp+ on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def blast(input_file, matrix, gapopen, gapextension, max_evalue, num_threads):
    name = input_file.split('/')[-1]
    # create output directory
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    try:
        os.mkdir(f"../program_out/{name}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"../program_out/{name}/blast")
    except FileExistsError:
        pass

    # run blast
    t1 = time.perf_counter()
    # TODO: threads, different comp_based_stats, note: doesn´t find a hit for each pair
    subprocess.run(f"blastp -query {input_file} -db {input_file} -gapopen {gapopen} -gapextend {gapextension} -matrix {matrix} -num_threads {num_threads} -evalue {max_evalue} -comp_based_stats 2  -max_hsps 1 -num_descriptions 1000000 -num_alignments 1000000 > ../program_out/{name}/blast/{name}.blast", shell=True)
    t2 = time.perf_counter()
    with open(f"../program_out/{name}/blast/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run blastp+ on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run blastp+ on the specified query/db file.')

    parser.add_argument("input",
        help="Input file path (used as query and db).")
    parser.add_argument("-m", "--matrix", default="BLOSUM50",
        help="Name of the substitution matrix: BLOSUM50 or BLOSUM62")
    parser.add_argument("-o", "--gapopen", type=int, default=15,
        help="Gap open penalty.")
    parser.add_argument("-e", "--gapextension", type=int, default=2,
        help="Gap extension penalty.")
    parser.add_argument("-v", "--max-evalue", type=int, default=20,
        help="Maximum e-value.")
    parser.add_argument("-t", "--num-threads", type=int, default=1,
        help="Number of CPU threads.")

    args = parser.parse_args()

    blast(args.input, args.matrix, args.gapopen, args.gapextension, args.max_evalue, args.num_threads)
 
if __name__ == '__main__':
    main()


# -matrix, supported matrices are:
# BLOSUM80
# BLOSUM62
# BLOSUM50
# BLOSUM45
# PAM250
# BLOSUM90
# PAM30
# PAM70
# IDENTITY

# BLAST query/options error: Gap existence and extension values of 10 and 1 not supported for blosum50
# supported values are:
# 32767, 32767
# 13, 3
# 12, 3
# 11, 3
# 10, 3
# 9, 3
# 16, 2
# 15, 2
# 14, 2
# 13, 2 <- simap2
# 12, 2
# 19, 1
# 18, 1
# 17, 1
# 16, 1
# 15, 1

# BLAST query/options error: Gap existence and extension values of 10 and 11 not supported for blosum62
# supported values are:
# 32767, 32767
# 11, 2
# 10, 2
# 9, 2
# 8, 2
# 7, 2
# 6, 2
# 13, 1
# 12, 1
# 11, 1
# 10, 1
# 9, 1