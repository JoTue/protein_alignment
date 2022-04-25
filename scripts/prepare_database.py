#!/usr/bin/env python3
"""Prepare a input FASTA-file (query/db) for the analysis of the protein alignment programs. 
change_fasta_header: renaming should allow uniform parsing of the headers of the alignment programs
split_multi_fasta: Split Multi-FASTA file into separate files (which can be used as queries for EMBOSS Water).
makeblastdb: BLAST database needed for SWIPE, BLASTp"""

import argparse
from Bio import SeqIO
from Bio.SeqIO import FastaIO
import os
import subprocess

def split_multi_fasta(input_file):
    name = input_file.split('/')[-1]
    try:
        os.mkdir(f"{input_file}_separate")
    except FileExistsError:
        pass

    for seq_record in SeqIO.parse(input_file, "fasta"):
        SeqIO.write(seq_record, f"{input_file}_separate/{seq_record.name}", "fasta")


def makeblastdb(input_file):
    subprocess.run(f"makeblastdb -blastdb_version 4 -dbtype prot -in {input_file} -out {input_file}", shell=True)


def change_fasta_header(input_file):
    # rename fasta header, should allow uniform parsing of the headers of the alignment programs
    with open(f"{os.path.dirname(input_file)}/corrected.fasta", 'w') as f:
        records = SeqIO.parse(input_file, 'fasta')
        for record in records:
            record.id = record.id.split("|")[-1].strip()
            record.description = record.description.split("|")[-1].strip()
            record_str = FastaIO.as_fasta_2line(record) # e.g. ADEPT fails to read multi-line records
            f.writelines(record_str)
    # overwrite old input_file
    os.remove(input_file)
    os.rename(f"{os.path.dirname(input_file)}/corrected.fasta", input_file)


def split_seqfile(input_file, num_threads, dir_name):
    # split input file into num_threads chunks
    chunk_n = int(subprocess.check_output(f"scripts/split_seqfile.py {input_file} -n {num_threads} -d {dir_name}", shell=True))
    # makeblastdb
    for chunk_i in range(1, chunk_n+1):
        subprocess.run(f"makeblastdb -blastdb_version 4 -dbtype prot -in {os.path.dirname(input_file)}/{dir_name}/q_{chunk_i} -out {os.path.dirname(input_file)}/{dir_name}/q_{chunk_i}", shell=True)


def split_seqfile_gpu(input_file, num_gpus, dir_name):
    # split input file into num_gpus chunks
    chunk_n = int(subprocess.check_output(f"scripts/split_seqfile.py {input_file} -n {num_gpus} -d {dir_name}", shell=True))


def main():
    """ 
    Prepare a input FASTA-file (query/db) for the analysis of the protein alignment programs.
    """
    parser = argparse.ArgumentParser(description = 'Prepare a input FASTA-file (query/db) for the analysis of the protein alignment programs.')

    parser.add_argument("input",
        help="Input file path.")
    parser.add_argument("-t", "--num-threads", type=int, default=1,
        help="Number of CPU threads.")
    parser.add_argument("-g", "--num-gpus", type=int, default=1,
        help="Number of GPUs.")

    args = parser.parse_args()

    change_fasta_header(args.input)
    split_multi_fasta(args.input) # water
    makeblastdb(args.input) # swipe, blast
    split_seqfile(args.input, args.num_threads, "qchunks")
    split_seqfile_gpu(args.input, args.num_gpus, "qchunks_gpu")
 
if __name__ == '__main__':
    main()
