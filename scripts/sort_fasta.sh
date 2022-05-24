#!/bin/sh

# sort input_file by decreasing sequence length (https://www.biostars.org/p/153999/)
# USAGE sort_fasta.sh input_file output_file

awk '/^>/ {printf("%s%s\t",(N>0?"\n":""),$0);N++;next;} {printf("%s",$0);} END {printf("\n");}' $1 | awk -F '\t' '{printf("%d\t%s\n",length($2),$0);}' | sort -k1,1nr | cut -f 2- | tr '\t' '\n' > $2
