#!/usr/bin/env python3
"""Parse swipe_xargs output files."""

import os
import argparse
import json
import sys

def swipe_xargs_parser(input_dir, TMPDIR):
    d = {}
    for input_file in os.scandir(f"{input_dir}"):
        if os.path.splitext(input_file)[1] == ".swipe_xargs":
            with open(input_file) as f:
                query, db, score = None, None, None
                for line in f:
                    if line.startswith("Query description:"):
                        query = line.split()[-1]
                    elif line.startswith(">"):
                        db = line.split()[-1]
                    elif line.startswith(" Score ="):
                        # if statistical parameters are not available for the scoring system specified. -> different parsing necessary
                        words = line.split()
                        if len(words) > 3:
                            score = float(words[4][1:-2])
                        else:
                            score = float(words[2])
                        d[query] = d.get(query, []) + [(db, score)]
            
    # write dictionary to json file
    name = input_dir.split('/')[-2]
    with open(f"{TMPDIR}/{name}/swipe_xargs/{name}.swipe_xargs.json", "w") as f:
        print(json.dumps(d), file=f)


def output_parser(input_dir, TMPDIR):
    name = input_dir.split('/')[-2]
    f_out = open(f"{TMPDIR}/{name}/swipe_xargs/{name}.swipe_xargs.results", "w")
    for input_file in os.scandir(f"{input_dir}"):
        if os.path.splitext(input_file)[1] == ".swipe_xargs":
            with open(input_file) as f:
                query, db, score = None, None, None
                for line in f:
                    if line.startswith("Query description:"):
                        query = line.split()[-1]
                    elif line.startswith(">"):
                        db = line.split()[-1]
                    elif line.startswith(" Score ="):
                        # if statistical parameters are not available for the scoring system specified. -> different parsing necessary
                        words = line.split()
                        if len(words) > 3:
                            score = float(words[4][1:-2])
                        else:
                            score = float(words[2])
                        f_out.write(f"{query}\t{db}\t{score}\n")
    f_out.close()            


def main():
    """ 
    Parse swipe_xargs output files.
    """
    parser = argparse.ArgumentParser(description = 'Parse swipe_xargs output files.')

    parser.add_argument("input",
        help="Path of the swipe_xargs output directory.")
    parser.add_argument("-d", "--tmp-dir", default=f"{os.path.dirname(os.path.dirname(sys.path[0]))}/program_out",
        help="Directory path used as temporary directory to read in files and write output.")

    args = parser.parse_args()

    output_parser(args.input, args.tmp_dir)
 
if __name__ == '__main__':
    main()