#!/usr/bin/env python3
"""Compute all-against-all protein sequence similarities of the specified database with various programs."""

import argparse
import subprocess
import os
import shutil


def call_programs(input_file, matrix, gapopen, gapextension, program_list):
    print("Start calling of alignment programs", flush=True)
    if "blast" in program_list:
        print("Running blast...", flush=True)
        subprocess.run(f"scripts/program_scripts/blast.py {input_file} -m {matrix} -o {gapopen} -e {gapextension}", shell=True)
    if "cudasw" in program_list:
        print("Running cudasw...", flush=True)
        subprocess.run(f"scripts/program_scripts/cudasw.py {input_file} -m {matrix} -o {gapopen} -e {gapextension}", shell=True)
    if "ssw" in program_list:
        print("Running ssw...", flush=True)
        subprocess.run(f"scripts/program_scripts/ssw.py {input_file} -m {matrix} -o {gapopen} -e {gapextension}", shell=True)
    if "swipe" in program_list:
        print("Running swipe...", flush=True)
        subprocess.run(f"scripts/program_scripts/swipe.py {input_file} -m {matrix} -o {gapopen} -e {gapextension}", shell=True)
    if "water" in program_list:
        print("Running water...", flush=True)
        subprocess.run(f"scripts/program_scripts/water.py {input_file} -m {matrix} -o {gapopen} -e {gapextension}", shell=True)
    if "adept" in program_list:
        print("Running adept...", flush=True)
        subprocess.run(f"scripts/program_scripts/adept.py {input_file} -m {matrix} -o {gapopen} -e {gapextension}", shell=True)
    if "adept_as" in program_list:
        print("Running adept_as...", flush=True)
        subprocess.run(f"scripts/program_scripts/adept_as.py {input_file} -m {matrix} -o {gapopen} -e {gapextension}", shell=True)


def call_output_parsers(input_file, program_list):
    name = input_file.split('/')[-1]
    print("Start parsing of output files", flush=True)
    if "blast" in program_list:
        print("Running blast_parser...", flush=True)
        subprocess.run(f"scripts/output_parsers/blast_parser.py program_out/{name}/blast/{name}.blast", shell=True)
    if "cudasw" in program_list:
        print("Running cudasw_parser...", flush=True)
        subprocess.run(f"scripts/output_parsers/cudasw_parser.py program_out/{name}/cudasw", shell=True)
    if "ssw" in program_list:
        print("Running ssw_parser...", flush=True)
        subprocess.run(f"scripts/output_parsers/ssw_parser.py program_out/{name}/ssw/{name}.ssw", shell=True)
    if "swipe" in program_list:
        print("Running swipe_parser...", flush=True)
        subprocess.run(f"scripts/output_parsers/swipe_parser.py program_out/{name}/swipe/{name}.swipe", shell=True)
    if "water" in program_list:
        print("Running water_parser...", flush=True)
        subprocess.run(f"scripts/output_parsers/water_parser.py program_out/{name}/water", shell=True)
    if "adept" in program_list:
        print("Running adept_parser...", flush=True)
        subprocess.run(f"scripts/output_parsers/adept_parser.py program_out/{name}/adept/{name}.adept", shell=True)
    if "adept_as" in program_list:
        print("Running adept_as_parser...", flush=True)
        subprocess.run(f"scripts/output_parsers/adept_as_parser.py program_out/{name}/adept_as/{name}.adept_as", shell=True)


def main():
    """ 
    Compute all-against-all protein sequence similarities of the specified database with various programs.
    """
    parser = argparse.ArgumentParser(description = 'Compute all-against-all protein sequence similarities of the specified database with various programs.')

    parser.add_argument("input",
        help="Input file path.")
    parser.add_argument("-m", "--matrix", default="BLOSUM50",
        help="Name of the substitution matrix: BLOSUM50 or BLOSUM62")
    parser.add_argument("-o", "--gapopen", type=int, default=15,
        help="Gap open penalty. Penalty for a gap of n positions: gap opening penalty + (n - 1) * gap extension penalty")
    parser.add_argument("-e", "--gapextension", type=int, default=2,
        help="Gap extension penalty.")
    parser.add_argument("-p", "--programs", nargs="+", default="all",
        help="List of programs to run. Default: blast, cudasw, ssw, swipe, water, adept, adept_as")
    parser.add_argument("-x", "--exact-programs", nargs="+", default="all",
        help="List of programs which should yield identical results (used for checking results). Default: cudasw, ssw, swipe, water, adept, adept_as")
    
    args = parser.parse_args()

    # create directory to store results
    name = args.input.split('/')[-1]
    print(f"Creating output directory: {os.path.abspath(f'program_out/{name}')}")
    os.chdir("/scratch/cube/tuechler/protein_alignment/")  # FIXME don´t hardcode
    try:
        os.mkdir(f"program_out/{name}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"program_out/{name}/data")
    except FileExistsError:
        pass
    # copy input file into program_out/{name}/data
    shutil.copy(args.input, f"program_out/{name}/data")
    input_file = f"program_out/{name}/data/{name}"

    # prepare database
    print("Running prepare_database.py...")
    subprocess.run(f"scripts/prepare_database.py {input_file}", shell=True)

    # create program_list
    if args.programs == "all":
        program_list = ["blast", "cudasw", "ssw", "swipe", "water", "adept", "adept_as"]
    else:
        program_list = args.programs
    program_string = " ".join(program_list)

    # create exact_programs
    if args.exact_programs == "all":
        exact_programs = ["cudasw", "ssw", "swipe", "water", "adept", "adept_as"]
    else:
        exact_programs = args.exact_programs
    exact_programs_string = " ".join(exact_programs)

    # write parameters summary file
    print("Writing parameters to parameters.txt")
    name = input_file.split('/')[-1]
    with open(f"program_out/{name}/parameters.txt", "w") as f:
        f.write(f"{input_file=}\n{args.matrix=}\n{args.gapopen=}\n{args.gapextension=}\n{program_list=}\n{exact_programs=}")

    # run alignment programs
    call_programs(input_file, args.matrix, args.gapopen, args.gapextension, program_list)

    # run output parsers
    call_output_parsers(input_file, program_list)

    subprocess.run(f"scripts/compare_results.py program_out/{name} program_out/{name}/data/{name} program_out/{name}/data/{name} -p {program_string} -x {exact_programs_string}", shell=True)

 
if __name__ == '__main__':
    main()