#!/usr/bin/env python3
"""Prepare a input FASTA-file (query/db) for the analysis of the protein alignment programs. 
split_multi_fasta: Split Multi-FASTA file into separate files (which can be used as queries for EMBOSS Water).
makeblastdb: BLAST database needed for SWIPE"""

import argparse
from Bio import SeqIO
import os
import subprocess

def split_multi_fasta(input_file):
    name = input_file.split('/')[-1]
    try:
        os.mkdir(f"{input_file}_separate")
    except FileExistsError:
        pass

    for seq_record in SeqIO.parse(input_file, "fasta"):
        SeqIO.write(seq_record, f"{input_file}_separate/{seq_record.name.replace('|', '_')}", "fasta")


def makeblastdb(input_file):
    subprocess.run(f"makeblastdb -blastdb_version 4 -dbtype prot -in {input_file} -out {input_file}", shell=True)


def main():
    """ 
    Prepare a input FASTA-file (query/db) for the analysis of the protein alignment programs.
    """
    parser = argparse.ArgumentParser(description = 'Prepare a input FASTA-file (query/db) for the analysis of the protein alignment programs.')

    parser.add_argument("input",
        help="Input file path.")

    args = parser.parse_args()

    split_multi_fasta(args.input) # water, cudasw
    makeblastdb(args.input) # swipe, blast
 
if __name__ == '__main__':
    main()
