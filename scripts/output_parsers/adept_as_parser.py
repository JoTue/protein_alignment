#!/usr/bin/env python3
"""Parse adept_as output file."""

import argparse
import json

def adept_as_parser(input_file):
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
    name = input_file.split('/')[-3]
    with open(f"../program_out/{name}/adept_as/{name}.adept_as.json", "w") as f:
        print(json.dumps(d), file=f)

            
def main():
    """ 
    Parse adept_as output file.
    """
    parser = argparse.ArgumentParser(description = 'Parse adept_as output file.')

    parser.add_argument("input",
        help="Path of the adept_as output file.")

    args = parser.parse_args()

    adept_as_parser(args.input)
 
if __name__ == '__main__':
    main()