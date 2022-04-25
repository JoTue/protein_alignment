#!/usr/bin/env python3
"""Split a FASTA file into #chunks files."""

import argparse
import os
import subprocess

def split_seqfile(input_file, chunk_n, dir_name):
    try:
        os.mkdir(f"{os.path.dirname(input_file)}/{dir_name}")
    except FileExistsError:
        pass

    seq_n = int(subprocess.check_output(f"grep -c '^>' {input_file}", shell=True))
    # compute chunk sizes, may be suboptimal if seq_n is small
    chunk_size = seq_n // chunk_n
    leftover = seq_n % chunk_n
    if chunk_size == 0:
        chunk_n = seq_n
        chunk_size = 1
        leftover = 0
    with open(input_file) as f:
        line = f.readline()
        for chunk_i in range(1, chunk_n+1):
            if chunk_i == (chunk_n):
                chunk_s = chunk_size + leftover
            else:
                chunk_s = chunk_size
            seq_c = 0
            with open(f"{os.path.dirname(input_file)}/{dir_name}/q_{chunk_i}", "w") as out_f:
                while seq_c < chunk_s:
                    if line == "":
                        break
                    if (line[0] == '>'):
                        header = line.strip()
                        line = f.readline()
                        continue
                    seq = line.strip()
                    out_f.write(f"{header}\n{seq}\n")
                    seq_c += 1
                    line = f.readline()
    print(chunk_n)

        
def main():
    """ 
    Prepare a input FASTA-file (query/db) for the analysis of the protein alignment programs.
    """
    parser = argparse.ArgumentParser(description = 'Prepare a input FASTA-file (query/db) for the analysis of the protein alignment programs.')

    parser.add_argument("input",
        help="Input file path.")
    parser.add_argument("-n", "--chunks", type=int,
        help="Number of chunks the input file is divided into.")
    parser.add_argument("-d", "--dir_name",
        help="Name of output directory.")

    args = parser.parse_args()

    split_seqfile(args.input, args.chunks, args.dir_name)
 
if __name__ == '__main__':
    main()
