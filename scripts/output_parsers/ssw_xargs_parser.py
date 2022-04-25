#!/usr/bin/env python3
"""Parse ssw output file."""

import os
import argparse
import json

def ssw_xargs_parser(input_dir):
    d = {}
    for input_file in os.scandir(f"{input_dir}"):
        if os.path.splitext(input_file)[1] == ".ssw_xargs":
            with open(input_file) as f:
                query, db, score = None, None, None
                for line in f:
                    if line.startswith("query_name:"):
                        query = line.split()[-1]
                    elif line.startswith("target_name:"):
                        db = line.split()[-1]
                    elif line.startswith("optimal"):
                        score = float(line.split()[1])
                        d[query] = d.get(query, []) + [(db, score)]
    
    # write dictionary to json file
    name = input_dir.split('/')[-2]
    with open(f"../program_out/{name}/ssw_xargs/{name}.ssw_xargs.json", "w") as f:
        print(json.dumps(d), file=f)


def main():
    """ 
    Parse ssw_xargs output files.
    """
    parser = argparse.ArgumentParser(description = 'Parse ssw_xargs output files.')

    parser.add_argument("input",
        help="Path of the ssw_xargs output directory.")

    args = parser.parse_args()

    ssw_xargs_parser(args.input)
 
if __name__ == '__main__':
    main()