#!/usr/bin/env python3
"""Split Multi-FASTA file into separate files (which can be used as queries for EMBOSS Water)."""

import argparse
from Bio import SeqIO
import os

input_file = "data/sp_n10_0_500"

def split_multi_fasta(input_file):
    try:
        os.mkdir(f"data/{input_file.split('/')[-1]}_separate")
    except FileExistsError:
        pass

    for seq_record in SeqIO.parse(input_file, "fasta"):
        SeqIO.write(seq_record, f"data/{input_file.split('/')[-1]}_separate/{seq_record.name.split('|')[-1]}.fasta", "fasta")


def main():
    """ 
    Split Multi-FASTA file into separate files.
    """
    parser = argparse.ArgumentParser(description = 'Split Multi-FASTA file into separate files.')

    parser.add_argument("input",
        help="Input file path.")

    args = parser.parse_args()

    split_multi_fasta(args.input)
 
if __name__ == '__main__':
    main()
