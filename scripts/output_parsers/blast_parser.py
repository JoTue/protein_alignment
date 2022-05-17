#!/usr/bin/env python3
"""Parse blast output file."""

import argparse
import json

def blast_parser(input_file):
    d = {}
    with open(input_file) as f:
        query, db, score = None, None, None
        for line in f:
            if line.startswith("Query="):
                query = line.split()[-1].strip()
            elif line.startswith(">"):
                db = line[1:].strip()
            elif line.startswith(" Score ="):
                score = float(line.split()[4][1:-2])
                d[query] = d.get(query, []) + [(db, score)]
    
    # write dictionary to json file
    name = input_file.split('/')[-3]
    with open(f"../program_out/{name}/blast/{name}.blast.json", "w") as f:
        print(json.dumps(d), file=f)

            
def main():
    """ 
    Parse blast output file.
    """
    parser = argparse.ArgumentParser(description = 'Parse blast output file.')

    parser.add_argument("input",
        help="Path of the blast output file.")

    args = parser.parse_args()

    blast_parser(args.input)
 
if __name__ == '__main__':
    main()