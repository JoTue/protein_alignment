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


def split_seqfile(input_file, chunk_n, chunk_s, dir_name):
    # split input file into chunks
    chunk_n = int(subprocess.check_output(f"scripts/split_seqfile.py {input_file} -n {chunk_n} -d {dir_name} -s {chunk_s}", shell=True))


def main():
    """ 
    Prepare a input FASTA-file (query/db) for the analysis of the protein alignment programs.
    """
    parser = argparse.ArgumentParser(description = 'Prepare a input FASTA-file (query/db) for the analysis of the protein alignment programs.')

    parser.add_argument("input", nargs="+",
        help="File paths of query and database files (space-separated). If only one file path is given, it will be used as query and database.")
    parser.add_argument("-t", "--num-threads", type=int, default=1,
        help="Number of CPU threads.")
    parser.add_argument("-g", "--num-gpus", type=int, default=1,
        help="Number of GPUs.")
    parser.add_argument("-p", "--programs", nargs="+", default="all",
        help="List of programs to run. Default: all")
    parser.add_argument("-s", "--chunksize", type=int, default=0,
        help="Maximal number of residues for each chunk used for xargs-scripts. If 0 (default) the chunknumber is equal to the thread/GPU number.")

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

    # create program_list
    if args.programs == "all":
        program_list = ["blast", "mmseqs", "water", "ssw", "ssw_xargs", "swipe", "swipe_xargs", "swipe_swlib_xargs", "cudasw", "cudasw_xargs", "adept", "adept_as", "adept_as_xargs"]
    else:
        program_list = args.programs

    change_fasta_header(query_file)
    change_fasta_header(db_file)
    if "water" in program_list:
        split_multi_fasta(query_file) # water
    # makeblastdb(query_file) # swipe, blast
    makeblastdb(db_file) # swipe, blast
    if args.chunksize:
        split_seqfile(query_file, 0, args.chunksize, "qchunks")
    else:
        split_seqfile(query_file, args.num_threads, args.chunksize, "qchunks_cpu")
        split_seqfile(query_file, args.num_gpus, args.chunksize, "qchunks_gpu")
 
if __name__ == '__main__':
    main()
