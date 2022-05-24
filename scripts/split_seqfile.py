#!/usr/bin/env python3
"""Split a FASTA file based on specified chunk-number or chunksize."""

import argparse
import os
import subprocess
import shutil

def split_seqfile(input_file, chunk_n, chunk_s, dir_name):
    input_file = os.path.abspath(input_file)
    if os.path.exists(f"{os.path.dirname(input_file)}/{dir_name}"):
        shutil.rmtree(f"{os.path.dirname(input_file)}/{dir_name}")
    os.makedirs(f"{os.path.dirname(input_file)}/{dir_name}")

    if chunk_n:
        """Split into chunk_n files.
        (split by aa number -> provides more equal chunk sizes compared to splitting by sequence number)
        This solution is not optimal, but should provide reasonably equal chunks."""
        # sort input_file by decreasing sequence length (https://www.biostars.org/p/153999/)
        sorted_input_file = f"{input_file}.sorted"
        subprocess.run(f"/scratch/cube/tuechler/protein_alignment/scripts/sort_fasta.sh {input_file} {sorted_input_file}", shell=True)
        # add sequences always to currently smallest chunk
        with open(sorted_input_file) as f:
            line = f.readline()
            writtenresidues = {chunk_i: 0 for chunk_i in range(1, chunk_n+1)}
            while line:
                if line == "":
                    break
                if (line[0] == '>'):
                    header = line.strip()
                    line = f.readline()
                    continue
                seq = line.strip()
                smallest_chunk_i = min(writtenresidues, key=writtenresidues.get)
                with open(f"{os.path.dirname(input_file)}/{dir_name}/q_{smallest_chunk_i}", "a") as out_f:
                    out_f.write(f"{header}\n{seq}\n")
                    writtenresidues[smallest_chunk_i] += len(seq)
                line = f.readline()
        actual_chunk_n = len(os.listdir(f"{os.path.dirname(input_file)}/{dir_name}"))
        print(actual_chunk_n)
    # OLD VERSION:
    # if chunk_n:
    #     """Split into chunk_n files (split by sequence number)"""
    #     seq_n = int(subprocess.check_output(f"grep -c '^>' {input_file}", shell=True))
    #     chunk_size = seq_n // chunk_n
    #     leftover = seq_n % chunk_n
    #     if chunk_size == 0:
    #         chunk_n = seq_n
    #         chunk_size = 1
    #         leftover = 0
    #     # chunk sizes differ maximal by 1 sequence:
    #     chunk_sizes = [chunk_size for _ in range(chunk_n)]
    #     for i in range(leftover):
    #         chunk_sizes[i] += 1
    #     with open(input_file) as f:
    #         line = f.readline()
    #         for chunk_i in range(1, chunk_n+1):
    #             current_chunk_size = chunk_sizes[chunk_i-1]
    #             seq_c = 0
    #             with open(f"{os.path.dirname(input_file)}/{dir_name}/q_{chunk_i}", "w") as out_f:
    #                 while seq_c < current_chunk_size:
    #                     if line == "":
    #                         break
    #                     if (line[0] == '>'):
    #                         header = line.strip()
    #                         line = f.readline()
    #                         continue
    #                     seq = line.strip()
    #                     out_f.write(f"{header}\n{seq}\n")
    #                     seq_c += 1
    #                     line = f.readline()
    #     print(chunk_n)
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
