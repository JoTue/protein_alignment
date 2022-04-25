#!/usr/bin/env python3
"""Parse cudasw output file."""

import os
import argparse
import json

def cudasw_xargs_parser(input_dir):
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
    with open(f"../program_out/{name}/cudasw_xargs/{name}.cudasw_xargs.json", "w") as f:
        print(json.dumps(d), file=f)


def main():
    """ 
    Parse cudasw output files.
    """
    parser = argparse.ArgumentParser(description = 'Parse cudasw output files.')

    parser.add_argument("input",
        help="Path of the cudasw_as_xargs output directory.")

    args = parser.parse_args()

    cudasw_xargs_parser(args.input)
 
if __name__ == '__main__':
    main()