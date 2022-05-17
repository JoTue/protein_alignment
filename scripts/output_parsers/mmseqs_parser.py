#!/usr/bin/env python3
"""Parse mmseqs output file."""

import os
import argparse
import json

def mmseqs_parser(input_file):
    d = {}
    with open(input_file) as f:
        query, db, score = None, None, None
        for line in f:
            words = line.split()
            if not words:
                break
            query = words[0]
            db = words[1]
            score = float(words[2])
            d[query] = d.get(query, []) + [(db, score)]
    
    # write dictionary to json file
    name = input_file.split('/')[-3]
    with open(f"../program_out/{name}/mmseqs/{name}.mmseqs.json", "w") as f:
        print(json.dumps(d), file=f)
            

def main():
    """ 
    Parse mmseqs output file.
    """
    parser = argparse.ArgumentParser(description = 'Parse mmseqs output file.')

    parser.add_argument("input",
        help="Path of the swipe output file.")

    args = parser.parse_args()

    mmseqs_parser(args.input)
 
if __name__ == '__main__':
    main()