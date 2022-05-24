#!/usr/bin/env python3
"""Parse cudasw output file."""

import os
import argparse
import json
import sys

def cudasw_parser(input_file, TMPDIR):
    d = {}
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
    name = input_file.split('/')[-3]
    with open(f"{TMPDIR}/{name}/cudasw/{name}.cudasw.json", "w") as f:
        print(json.dumps(d), file=f)


def output_parser(input_file, TMPDIR):
    name = input_file.split('/')[-3]
    f_out = open(f"{TMPDIR}/{name}/cudasw/{name}.cudasw.results", "w")
    with open(input_file) as f:
        query, db, score = None, None, None
        for line in f:
            if line.startswith("query:"):
                query = line[6:].strip()
            elif line.startswith("score:"):
                words = line.split()
                db = words[3]
                score = float(words[1])
                f_out.write(f"{query}\t{db}\t{score}\n")
    f_out.close()


def main():
    """ 
    Parse cudasw output file.
    """
    parser = argparse.ArgumentParser(description = 'Parse cudasw output file.')

    # parser.add_argument("input",
    #     help="Path of the cudasw output directory.")
    parser.add_argument("input",
        help="Path of the ssw output file.")
    parser.add_argument("-d", "--tmp-dir", default=f"{os.path.dirname(os.path.dirname(sys.path[0]))}/program_out",
        help="Directory path used as temporary directory to read in files and write output.")

    args = parser.parse_args()

    output_parser(args.input, args.tmp_dir)
 
if __name__ == '__main__':
    main()