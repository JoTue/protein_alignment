#!/usr/bin/env python3
"""Parse adept_as_xargs output file."""

import os
import argparse
import json
import sys

def adept_as_xargs_parser(input_dir, TMPDIR):
    d = {}
    for input_file in os.scandir(f"{input_dir}"):
        if os.path.splitext(input_file)[1] == ".adept_as_xargs":
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
    name = input_dir.split('/')[-2]
    with open(f"{TMPDIR}/{name}/adept_as_xargs/{name}.adept_as_xargs.json", "w") as f:
        print(json.dumps(d), file=f)

            
def output_parser(input_dir, TMPDIR):
    name = input_dir.split('/')[-2]
    f_out = open(f"{TMPDIR}/{name}/adept_as_xargs/{name}.adept_as_xargs.results", "w")
    for input_file in os.scandir(f"{input_dir}"):
        if os.path.splitext(input_file)[1] == ".adept_as_xargs":
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
    Parse adept_as_xargs output files.
    """
    parser = argparse.ArgumentParser(description = 'Parse adept_as_xargs output files.')

    parser.add_argument("input",
        help="Path of the adept_as_xargs output directory.")
    parser.add_argument("-d", "--tmp-dir", default=f"{os.path.dirname(os.path.dirname(sys.path[0]))}/program_out",
        help="Directory path used as temporary directory to read in files and write output.")

    args = parser.parse_args()

    output_parser(args.input, args.tmp_dir)
 
if __name__ == '__main__':
    main()