#!/usr/bin/env python3
"""Run water on the specified query/db file"""

import subprocess
import os
import time
import argparse
import sys

def water(input_file, matrix, gapopen, gapextension):
    name = input_file.split('/')[-1]
    # create output directory
    os.chdir(os.path.dirname(os.path.dirname(sys.path[0])))
    try:
        os.mkdir(f"../program_out/{name}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"../program_out/{name}/water")
    except FileExistsError:
        pass

    # run water
    t1 = time.perf_counter()
    for query in os.scandir(f"{input_file}_separate"):
        subprocess.run(f"water {query.path} {input_file} -gapopen {gapopen} -gapextend {gapextension} -datafile /apps/emboss/6.6.0/emboss/data/E{matrix} -sprotein -aformat score -outfile ../program_out/{name}/water/{query.name}.water", shell=True) # add to supress messages to stdout: >/dev/null 2>&1
    t2 = time.perf_counter()
    with open(f"../program_out/{name}/water/time.txt", "w") as f:
        f.write(f"{t2 - t1}")


def main():
    """ 
    Run water on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run water on the specified query/db file.')

    parser.add_argument("input",
        help="Input file path (used as query and db).")
    parser.add_argument("-m", "--matrix", default="BLOSUM50",
        help="Name of the substitution matrix: BLOSUM50 or BLOSUM62")
    parser.add_argument("-o", "--gapopen", type=int, default=15,
        help="Gap open penalty.")
    parser.add_argument("-e", "--gapextension", type=int, default=2,
        help="Gap extension penalty.")

    args = parser.parse_args()

    water(args.input, args.matrix, args.gapopen, args.gapextension)
 
if __name__ == '__main__':
    main()
