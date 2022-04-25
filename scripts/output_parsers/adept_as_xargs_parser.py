#!/usr/bin/env python3
"""Parse adept_as_xargs output file."""

import os
import argparse
import json

def adept_as_xargs_parser(input_dir):
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
    with open(f"../program_out/{name}/adept_as_xargs/{name}.adept_as_xargs.json", "w") as f:
        print(json.dumps(d), file=f)

            
def main():
    """ 
    Parse adept_as_xargs output files.
    """
    parser = argparse.ArgumentParser(description = 'Parse adept_as_xargs output files.')

    parser.add_argument("input",
        help="Path of the adept_as_xargs output directory.")

    args = parser.parse_args()

    adept_as_xargs_parser(args.input)
 
if __name__ == '__main__':
    main()