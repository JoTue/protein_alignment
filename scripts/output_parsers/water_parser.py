#!/usr/bin/env python3
"""Parse water output files."""

import os
import argparse
import json

def water_parser(input_dir):
    d = {}
    for input_file in os.scandir(f"{input_dir}"):
        if os.path.splitext(input_file)[1] == ".water":
            with open(input_file) as f:
                query, db, score = None, None, None
                for line in f:
                    words = line.split()
                    if not words:
                        break
                    query = words[0]
                    db = words[1]
                    score = float(words[-1][1:-1])
                    d[query] = d.get(query, []) + [(db, score)]
    
    # write dictionary to json file
    name = input_dir.split('/')[-2]
    with open(f"../program_out/{name}/water/{name}.water.json", "w") as f:
        print(json.dumps(d), file=f)
            

def main():
    """ 
    Parse water output files.
    """
    parser = argparse.ArgumentParser(description = 'Parse water output files.')

    parser.add_argument("input",
        help="Path of the water output directory.")

    args = parser.parse_args()

    water_parser(args.input)
 
if __name__ == '__main__':
    main()