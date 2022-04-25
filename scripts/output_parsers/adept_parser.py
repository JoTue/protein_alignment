#!/usr/bin/env python3
"""Parse adept output file."""

import argparse
import json

# FIXME: different format if multiple gpus are used

def adept_parser(input_file):
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
    name = input_file.split('/')[-1].split(".")[0]
    with open(f"../program_out/{name}/adept/{name}.adept.json", "w") as f:
        print(json.dumps(d), file=f)

            
def main():
    """ 
    Parse adept output file.
    """
    parser = argparse.ArgumentParser(description = 'Parse adept output file.')

    parser.add_argument("input",
        help="Path of the adept output file.")

    args = parser.parse_args()

    adept_parser(args.input)
 
if __name__ == '__main__':
    main()