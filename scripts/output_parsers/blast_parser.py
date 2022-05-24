#!/usr/bin/env python3
"""Parse blast output file."""

import os
import argparse
import json
import sys

def blast_parser(input_file, TMPDIR):
    d = {}
    with open(input_file) as f:
        query, db, score = None, None, None
        for line in f:
            if line.startswith("Query="):
                query = line.split()[-1].strip()
            elif line.startswith(">"):
                db = line[1:].strip()
            elif line.startswith(" Score ="):
                score = float(line.split()[4][1:-2])
                d[query] = d.get(query, []) + [(db, score)]
    
    # write dictionary to json file
    name = input_file.split('/')[-3]
    with open(f"{TMPDIR}/{name}/blast/{name}.blast.json", "w") as f:
        print(json.dumps(d), file=f)


def output_parser(input_file, TMPDIR):
    name = input_file.split('/')[-3]
    f_out = open(f"{TMPDIR}/{name}/blast/{name}.blast.results", "w")
    with open(input_file) as f:
        query, db, score = None, None, None
        for line in f:
            if line.startswith("Query="):
                query = line.split()[-1].strip()
            elif line.startswith(">"):
                db = line[1:].strip()
            elif line.startswith(" Score ="):
                score = float(line.split()[4][1:-2])
                f_out.write(f"{query}\t{db}\t{score}\n")
    f_out.close()
    
            
def main():
    """ 
    Parse blast output file.
    """
    parser = argparse.ArgumentParser(description = 'Parse blast output file.')

    parser.add_argument("input",
        help="Path of the blast output file.")
    parser.add_argument("-d", "--tmp-dir", default=f"{os.path.dirname(os.path.dirname(sys.path[0]))}/program_out",
        help="Directory path used as temporary directory to read in files and write output.")

    args = parser.parse_args()

    output_parser(args.input, args.tmp_dir)
 
if __name__ == '__main__':
    main()