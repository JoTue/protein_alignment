#!/usr/bin/env python3
"""Parse cudasw output file."""

import os
import argparse
import json
import sys

def cudasw_xargs_parser(input_dir, TMPDIR):
    d = {}
    for input_file in os.scandir(f"{input_dir}"):
        if os.path.splitext(input_file)[1] == ".cudasw_xargs":
            with open(input_file) as f:
                query, db, score = None, None, None
                for line in f:
                    if line.startswith("query:"):
                        query = line[6:].strip()
                    elif line.startswith("score:"):
                        words = line.split()
                        db = words[3]
                        score = float(words[1])
                        d[query] = d.get(query, []) + [(db, score)]
                        
    # write dictionary to json file
    name = input_dir.split('/')[-2]
    with open(f"{TMPDIR}/{name}/cudasw_xargs/{name}.cudasw_xargs.json", "w") as f:
        print(json.dumps(d), file=f)


def output_parser(input_dir, TMPDIR):
    name = input_dir.split('/')[-2]
    f_out = open(f"{TMPDIR}/{name}/cudasw_xargs/{name}.cudasw_xargs.results", "w")
    for input_file in os.scandir(f"{input_dir}"):
        if os.path.splitext(input_file)[1] == ".cudasw_xargs":
            with open(input_file) as f:
                query, db, score = None, None, None
                for line in f:
                    if line.startswith("query:"):
                        query = line[6:].strip()
                    elif line.startswith("score:"):
                        words = line.split()
                        db = words[3]
                        score = float(words[1])
                        f_out.write(f"{query}\t{db}\t{score}\n")
    f_out.close()


def main():
    """ 
    Parse cudasw output files.
    """
    parser = argparse.ArgumentParser(description = 'Parse cudasw output files.')

    parser.add_argument("input",
        help="Path of the cudasw_as_xargs output directory.")
    parser.add_argument("-d", "--tmp-dir", default=f"{os.path.dirname(os.path.dirname(sys.path[0]))}/program_out",
        help="Directory path used as temporary directory to read in files and write output.")

    args = parser.parse_args()

    output_parser(args.input, args.tmp_dir)
 
if __name__ == '__main__':
    main()