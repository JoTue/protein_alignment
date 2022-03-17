"""Split query-multi-FASTA file into separate files, which can be used for EMBOSS Water."""

from Bio import SeqIO
import os

input_file = "data/sp_n10_0_400"

try:
    os.mkdir(f"data/{input_file.split('/')[-1]}_queries")
except FileExistsError:
    pass

for seq_record in SeqIO.parse(input_file, "fasta"):
    SeqIO.write(seq_record, f"data/{input_file.split('/')[-1]}_queries/{seq_record.name}.fasta", "fasta")
