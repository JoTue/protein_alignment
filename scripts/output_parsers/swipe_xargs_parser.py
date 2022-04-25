#!/usr/bin/env python3
"""Parse swipe_xargs output files."""

import os
import argparse
import json

def swipe_xargs_parser(input_dir):
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
    with open(f"../program_out/{name}/swipe_xargs/{name}.swipe_xargs.json", "w") as f:
        print(json.dumps(d), file=f)

            

def main():
    """ 
    Parse swipe_xargs output files.
    """
    parser = argparse.ArgumentParser(description = 'Parse swipe_xargs output files.')

    parser.add_argument("input",
        help="Path of the swipe_xargs output directory.")

    args = parser.parse_args()

    swipe_xargs_parser(args.input)
 
if __name__ == '__main__':
    main()