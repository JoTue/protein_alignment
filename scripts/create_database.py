#!/usr/bin/env python3

import argparse
import subprocess
import shutil
import os
from Bio import SeqIO
import re

def create_database(n, min_len, max_len, input_file, output_file):
    tmp_file = "tmp_file"
    tmp_file2 = "tmp_file2"
    # filter by length
    if min_len or max_len:
        if not min_len:
            min_len = 0
        if not max_len:
            max_len = 1e9
        subprocess.run(f"""bioawk -c fastx '{{ if (length($seq) >= {min_len} && length($seq) <= {max_len}) {{ print ">"$name; print $seq }}}}' {input_file} > {tmp_file}""", shell=True)
    else:
        shutil.copyfile(input_file, tmp_file)
    # filter out sequences with non-standard aa
    reg = re.compile('^[ACDEFGHIKLMNPQRSTVWY]+$')
    seq_records = [rec for rec in SeqIO.parse(tmp_file, "fasta") if reg.match(str(rec.seq))]
    SeqIO.write(seq_records, tmp_file2, "fasta")
    # retain n random sequences
    if n:
        subprocess.run(f"""bioawk -c fastx -v k={n} '{{y=x++<k?x-1:int(rand()*x);if(y<k)a[y]=">"$name"\\n"$seq}}END{{for(z in a)print a[z]}}' {tmp_file2} > {output_file}""", shell=True)
    else:
        shutil.copyfile(tmp_file2, output_file)
    os.remove(tmp_file)
    os.remove(tmp_file2)
    seq_n = int(subprocess.check_output(f"grep -c '^>' {output_file}", shell=True))
    print(f"Output file contains {seq_n} sequences.")


def main():
    """ 
    Creates a random subsample of a database in FASTA-format.
    """
    parser = argparse.ArgumentParser(description = 'Creates a random subsample of a database in FASTA-format.')

    parser.add_argument("-n", type=int,
        help="Number of sequences in new database")
    parser.add_argument("--min-len", type=int,
        help="Minimal sequence length of new database entries.")
    parser.add_argument("--max-len", type=int,
        help="Maximal sequence length of new database entries.")
    parser.add_argument("input",
        help="Input file path.")
    parser.add_argument("output",
        help="Output file path.")
    args = parser.parse_args()

    create_database(args.n, args.min_len, args.max_len, args.input, args.output)
 
if __name__ == '__main__':
    main()
