#!/usr/bin/env python3
"""Split a FASTA file based on specified chunk-number or chunksize."""

import argparse
import os
import subprocess

def split_seqfile(input_file, chunk_n, chunk_s, dir_name):
    try:
        os.mkdir(f"{os.path.dirname(input_file)}/{dir_name}")
    except FileExistsError:
        pass

    if chunk_n:
        """Split into chunk_n files"""
        seq_n = int(subprocess.check_output(f"grep -c '^>' {input_file}", shell=True))
        chunk_size = seq_n // chunk_n
        leftover = seq_n % chunk_n
        if chunk_size == 0:
            chunk_n = seq_n
            chunk_size = 1
            leftover = 0
        # chunk sizes differ maximal by 1 sequence:
        chunk_sizes = [chunk_size for _ in range(chunk_n)]
        for i in range(leftover):
            chunk_sizes[i] += 1
        with open(input_file) as f:
            line = f.readline()
            for chunk_i in range(1, chunk_n+1):
                current_chunk_size = chunk_sizes[chunk_i-1]
                seq_c = 0
                with open(f"{os.path.dirname(input_file)}/{dir_name}/q_{chunk_i}", "w") as out_f:
                    while seq_c < current_chunk_size:
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
    elif chunk_s:
        """Split into chunks with maximal chunk_s residues each."""
        # if a single entry is longer than chunk_s it is written to a separate chunk - this chunk is then bigger than chunk_s
        with open(input_file) as f:
            line = f.readline()
            chunk_i = 1
            out_f = open(f"{os.path.dirname(input_file)}/{dir_name}/q_{chunk_i}", "w")
            writtenresidues = 0
            while line:
                if line == "":
                    break
                if (line[0] == '>'):
                    header = line.strip()
                    line = f.readline()
                    continue
                seq = line.strip()
                if writtenresidues + len(seq) > chunk_s and writtenresidues:
                    out_f.close()
                    chunk_i += 1
                    out_f = open(f"{os.path.dirname(input_file)}/{dir_name}/q_{chunk_i}", "w")
                    out_f.write(f"{header}\n{seq}\n")
                    writtenresidues = len(seq)
                else:
                    out_f.write(f"{header}\n{seq}\n")
                    writtenresidues += len(seq)
                line = f.readline()
        out_f.close()
        print(chunk_i)
    else:
        raise Exception("Input chunknumber or chunksize.")

        
def main():
    """ 
    Split a FASTA file based on specified chunk-number or chunksize.
    """
    parser = argparse.ArgumentParser(description = 'Split a FASTA file based on specified chunk-number or chunksize.')

    parser.add_argument("input",
        help="Input file path.")
    parser.add_argument("-n", "--chunknumber", type=int,
        help="Number of chunks the input file is divided into.")
    parser.add_argument("-s", "--chunksize", type=int,
        help="Split into chunks with up to chunksize amino acids.")
    parser.add_argument("-d", "--dir_name",
        help="Name of output directory.")

    args = parser.parse_args()

    split_seqfile(args.input, args.chunknumber, args.chunksize, args.dir_name)
 
if __name__ == '__main__':
    main()
