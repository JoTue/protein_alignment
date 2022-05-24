#!/usr/bin/env python3
"""Parse adept output file."""

import os
import argparse
import json
import sys

def adept_parser(input_file, TMPDIR):
    d = {}
    with open(input_file) as f:
        query, db, score = None, None, None
        f.readline() # skip header line
        for line in f:
            words = line.split()
            if not words:
                break
            query = words[6]
            db = words[5]
            score = float(words[0].strip("[]"))
            d[query] = d.get(query, []) + [(db, score)]
    
    # write dictionary to json file
    name = input_file.split('/')[-3]
    with open(f"{TMPDIR}/{name}/adept/{name}.adept.json", "w") as f:
        print(json.dumps(d), file=f)


def output_parser(input_file, TMPDIR):
    name = input_file.split('/')[-3]
    f_out = open(f"{TMPDIR}/{name}/adept/{name}.adept.results", "w")
    with open(input_file) as f:
        query, db, score = None, None, None
        f.readline() # skip header line
        for line in f:
            words = line.split()
            if not words:
                break
            query = words[6]
            db = words[5]
            score = float(words[0].strip("[]"))
            f_out.write(f"{query}\t{db}\t{score}\n")
    f_out.close()
            
            
def main():
    """ 
    Parse adept output file.
    """
    parser = argparse.ArgumentParser(description = 'Parse adept output file.')

    parser.add_argument("input",
        help="Path of the adept output file.")
    parser.add_argument("-d", "--tmp-dir", default=f"{os.path.dirname(os.path.dirname(sys.path[0]))}/program_out",
        help="Directory path used as temporary directory to read in files and write output.")

    args = parser.parse_args()

    output_parser(args.input, args.tmp_dir)
 
if __name__ == '__main__':
    main()