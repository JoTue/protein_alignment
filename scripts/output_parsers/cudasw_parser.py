#!/usr/bin/env python3
"""Parse cudasw output file."""

import os
import argparse
import json

def cudasw_parser(input_file):
    d = {}
    # for input_file in os.scandir(f"{input_dir}"):
    #     if os.path.splitext(input_file)[1] == ".cudasw":
    #         with open(input_file) as f:
    #             query, db, score = None, None, None
    #             for line in f:
    #                 if line.startswith("query:"):
    #                     query = line[6:].strip()
    #                 elif line.startswith("score:"):
    #                     words = line.split()
    #                     db = words[3]
    #                     score = float(words[1])
    #                     d[query] = d.get(query, []) + [(db, score)]
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
    name = input_file.split('/')[-1].split(".")[0]
    with open(f"../program_out/{name}/cudasw/{name}.cudasw.json", "w") as f:
        print(json.dumps(d), file=f)


def main():
    """ 
    Parse cudasw output file.
    """
    parser = argparse.ArgumentParser(description = 'Parse cudasw output file.')

    # parser.add_argument("input",
    #     help="Path of the cudasw output directory.")
    parser.add_argument("input",
        help="Path of the ssw output file.")

    args = parser.parse_args()

    cudasw_parser(args.input)
 
if __name__ == '__main__':
    main()