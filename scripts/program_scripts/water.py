#!/usr/bin/env python3
"""Run EMBOSS Water on the specified query/db file"""

import subprocess
import os
import time
import argparse

def water(input_file):
    # split multi-fasta file into separate single-fasta files (stored in data/<input_file>_separate)
    subprocess.run(f"scripts/prepare_water_queries.py {input_file}", shell=True)

    # create output directory
    try:
        os.mkdir(f"program_out/water/{input_file.split('/')[-1]}")
    except FileExistsError:
        pass


    # run water
    t1 = time.perf_counter()
    for query in os.scandir(f"{input_file}_separate"):
        subprocess.run(f"water {query.path} {input_file} -gapopen 10 -gapextend 0.5 -outfile program_out/water/{input_file.split('/')[-1]}/{query.name}.water -aformat srspair", shell=True) # add to supress messages to stdout: >/dev/null 2>&1
    t2 = time.perf_counter()
    with open(f"program_out/water/{input_file.split('/')[-1]}/time.txt", "w") as f:
        f.write(f"{t2 - t1}")

def main():
    """ 
    Run EMBOSS Water on the specified query/db file.
    """
    parser = argparse.ArgumentParser(description = 'Run EMBOSS Water on the specified query/db file.')

    parser.add_argument("input",
        help="Input file path (used as query and db).")

    args = parser.parse_args()

    water(args.input)
 
if __name__ == '__main__':
    main()