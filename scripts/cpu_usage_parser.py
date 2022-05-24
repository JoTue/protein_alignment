#!/usr/bin/env python3
"""Retrieve CPU usage of programs, and write summary to file."""

import os
import argparse
import sys


def cpu_usage_parser(input_file, TMPDIR, program_list, name):
    program = None
    print("CPU usage of programs (in %):")
    with open(input_file) as f:
        for line in f:
            if line.startswith("Creating temporary directory: "):
                parsed_name = line.split("/")[-1].strip()
                if parsed_name == name:
                    f_out = open(f"{TMPDIR}/{name}/cpu_usage.txt", "w")
                    break
        for line in f:
            if line.startswith("Running "):
                word = line.split()[1].strip()[:-3]
                if word in program_list:
                    program = word
                else:
                    program = None
                continue
            if "%CPU (" in line and program:
                cpu_usage = int(line.split()[3].split("%")[0])
                print(f"{str(program+':').ljust(20)}{cpu_usage}")
                f_out.write(f"{str(program+':').ljust(20)}{cpu_usage}\n")
                continue
    f_out.close()

            
def main():
    """ 
    Retrieve CPU usage of programs, and write summary to file.
    """
    parser = argparse.ArgumentParser(description = 'Retrieve CPU usage of programs, and write summary to file.')

    parser.add_argument("input",
        help="Path of the SLURM output file.")
    parser.add_argument("-n", "--name", default=None,
        help="Name of output directory. ") 
    parser.add_argument("-d", "--tmp-dir", default=f"{os.path.dirname(os.path.dirname(sys.path[0]))}/program_out",
        help="Directory path used as temporary directory to read in files and write output.")
    parser.add_argument("-p", "--programs", nargs="+", default="all",
        help="List of programs to run. Default: all")

    args = parser.parse_args()

    # create program_list
    if args.programs == "all":
        program_list = ["blast", "mmseqs", "water", "ssw", "ssw_xargs", "swipe", "swipe_xargs", "swipe_swlib_xargs", "cudasw", "cudasw_xargs", "adept", "adept_as", "adept_as_xargs"]
    else:
        program_list = args.programs

    cpu_usage_parser(args.input, args.tmp_dir, program_list, args.name)
 
if __name__ == '__main__':
    main()