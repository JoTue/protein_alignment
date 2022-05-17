#!/usr/bin/env python3
"""Parse swipe output file."""

import argparse
import json

def swipe_parser(input_file):
    d = {}
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
    name = input_file.split('/')[-3]
    with open(f"../program_out/{name}/swipe/{name}.swipe.json", "w") as f:
        print(json.dumps(d), file=f)

            

def main():
    """ 
    Parse swipe output file.
    """
    parser = argparse.ArgumentParser(description = 'Parse swipe output file.')

    parser.add_argument("input",
        help="Path of the swipe output file.")

    args = parser.parse_args()

    swipe_parser(args.input)
 
if __name__ == '__main__':
    main()