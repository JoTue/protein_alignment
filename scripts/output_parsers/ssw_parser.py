#!/usr/bin/env python3
"""Parse ssw output file."""

import argparse
import json

def ssw_parser(input_file):
    d = {}
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
    name = input_file.split('/')[-3]
    with open(f"../program_out/{name}/ssw/{name}.ssw.json", "w") as f:
        print(json.dumps(d), file=f)
            

def main():
    """ 
    Parse ssw output file.
    """
    parser = argparse.ArgumentParser(description = 'Parse ssw output file.')

    parser.add_argument("input",
        help="Path of the ssw output file.")

    args = parser.parse_args()

    ssw_parser(args.input)
 
if __name__ == '__main__':
    main()