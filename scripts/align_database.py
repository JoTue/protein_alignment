#!/usr/bin/env python3
"""Compute all-against-all protein sequence similarities of the specified database with various programs."""

import argparse
import subprocess
import os
import shutil
import sys


def call_programs(input_file, matrix, gapopen, gapextension, min_score, max_evalue, num_threads, num_gpus, program_list):
    print("Start calling of alignment programs", flush=True)
    if "blast" in program_list:
        print("Running blast...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/blast.py {input_file} -m {matrix} -o {gapopen} -e {gapextension} -v {max_evalue} -t {num_threads}", shell=True)
    if "mmseqs" in program_list:
        print("Running mmseqs...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/mmseqs.py {input_file} -m {matrix} -o {gapopen} -e {gapextension} -v {max_evalue} -t {num_threads}", shell=True)
    if "cudasw" in program_list:
        print("Running cudasw...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/cudasw.py {input_file} -m {matrix} -o {gapopen} -e {gapextension} -t {num_threads} -g {num_gpus} -c {min_score}", shell=True)
    if "cudasw_xargs" in program_list:
        print("Running cudasw_xargs...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/cudasw_xargs.py {input_file} -m {matrix} -o {gapopen} -e {gapextension} -t {num_threads} -g {num_gpus} -c {min_score}", shell=True)
    if "ssw" in program_list:
        print("Running ssw...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/ssw.py {input_file} -m {matrix} -o {gapopen} -e {gapextension} -c {min_score}", shell=True)
    if "ssw_xargs" in program_list:
        print("Running ssw_xargs...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/ssw_xargs.py {input_file} -m {matrix} -o {gapopen} -e {gapextension} -t {num_threads} -c {min_score}", shell=True)
    if "swipe" in program_list:
        print("Running swipe...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/swipe.py {input_file} -m {matrix} -o {gapopen} -e {gapextension} -t {num_threads} -c {min_score}", shell=True)
    if "swipe_xargs" in program_list:
        print("Running swipe_xargs...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/swipe_xargs.py {input_file} -m {matrix} -o {gapopen} -e {gapextension} -t {num_threads} -c {min_score}", shell=True)
    if "water" in program_list:
        print("Running water...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/water.py {input_file} -m {matrix} -o {gapopen} -e {gapextension}", shell=True)
    if "adept" in program_list:
        print("Running adept...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/adept.py {input_file} -m {matrix} -o {gapopen} -e {gapextension}", shell=True)
    if "adept_as" in program_list:
        print("Running adept_as...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/adept_as.py {input_file} -m {matrix} -o {gapopen} -e {gapextension}", shell=True)
    if "adept_as_xargs" in program_list:
        print("Running adept_as_xargs...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/adept_as_xargs.py {input_file} -m {matrix} -o {gapopen} -e {gapextension} -g {num_gpus}", shell=True)


def call_output_parsers(input_file, program_list):
    name = input_file.split('/')[-1]
    print("Start parsing of output files", flush=True)
    if "blast" in program_list:
        print("Running blast_parser...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/output_parsers/blast_parser.py ../program_out/{name}/blast/{name}.blast", shell=True)
    if "mmseqs" in program_list:
        print("Running mmseqs_parser...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/output_parsers/mmseqs_parser.py ../program_out/{name}/mmseqs/{name}.mmseqs", shell=True)
    if "cudasw" in program_list:
        print("Running cudasw_parser...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/output_parsers/cudasw_parser.py ../program_out/{name}/cudasw/{name}.cudasw", shell=True)
    if "cudasw_xargs" in program_list:
        print("Running cudasw_xargs_parser...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/output_parsers/cudasw_xargs_parser.py ../program_out/{name}/cudasw_xargs", shell=True)
    if "ssw" in program_list:
        print("Running ssw_parser...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/output_parsers/ssw_parser.py ../program_out/{name}/ssw/{name}.ssw", shell=True)
    if "ssw_xargs" in program_list:
        print("Running ssw_xargs_parser...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/output_parsers/ssw_xargs_parser.py ../program_out/{name}/ssw_xargs", shell=True)
    if "swipe" in program_list:
        print("Running swipe_parser...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/output_parsers/swipe_parser.py ../program_out/{name}/swipe/{name}.swipe", shell=True)
    if "swipe_xargs" in program_list:
        print("Running swipe_xargs_parser...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/output_parsers/swipe_xargs_parser.py ../program_out/{name}/swipe_xargs", shell=True)
    if "water" in program_list:
        print("Running water_parser...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/output_parsers/water_parser.py ../program_out/{name}/water", shell=True)
    if "adept" in program_list:
        print("Running adept_parser...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/output_parsers/adept_parser.py ../program_out/{name}/adept/{name}.adept", shell=True)
    if "adept_as" in program_list:
        print("Running adept_as_parser...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/output_parsers/adept_as_parser.py ../program_out/{name}/adept_as/{name}.adept_as", shell=True)
    if "adept_as_xargs" in program_list:
        print("Running adept_as_xargs_parser...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/output_parsers/adept_as_xargs_parser.py ../program_out/{name}/adept_as_xargs", shell=True)


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
    parser.add_argument("-c", "--min-score", type=int, default=50,
        help="Minimimum score of alignments to show.")
    parser.add_argument("-v", "--max-evalue", type=int, default=20,
        help="Maximum e-value.")
    parser.add_argument("-t", "--num-threads", type=int, default=1,
        help="Number of CPU threads.")
    parser.add_argument("-g", "--num-gpus", type=int, default=1,
        help="Number of GPUs.")
    parser.add_argument("-p", "--programs", nargs="+", default="all",
        help="List of programs to run. Default: all")
    parser.add_argument("-x", "--exact-programs", nargs="+", default="all",
        help="List of programs which should yield identical results (used for checking results). Default: all SW implementations")
    parser.add_argument("-r", "--only-runtime", action = "store_true", 
        help="Do not compare scores of the exact programs.")

    args = parser.parse_args()

    # create directory to store results, and change working directory
    name = args.input.split('/')[-1]
    print(f"Creating output directory: {os.path.abspath(f'../program_out/{name}')}")
    os.chdir(os.path.dirname(sys.path[0]))
    if os.path.exists(f"../program_out/{name}"):
        shutil.rmtree(f"../program_out/{name}")
    os.makedirs(f"../program_out/{name}/data")

    # copy input file into program_out/{name}/data
    shutil.copy(args.input, f"../program_out/{name}/data")
    input_file = f"../program_out/{name}/data/{name}"

    # prepare database
    print("Running prepare_database.py...")
    subprocess.run(f"scripts/prepare_database.py {input_file} -t {args.num_threads} -g {args.num_gpus}", shell=True)

    # create program_list
    if args.programs == "all":
        program_list = ["blast", "cudasw", "cudasw_xargs", "ssw", "ssw_xargs", "swipe", "swipe_xargs", "water", "adept", "adept_as", "adept_as_xargs", "mmseqs"]
    else:
        program_list = args.programs
    program_string = " ".join(program_list)

    # create exact_programs
    if args.exact_programs == "all":
        exact_programs = ["cudasw", "cudasw_xargs", "ssw", "ssw_xargs", "swipe", "swipe_xargs", "water", "adept", "adept_as", "adept_as_xargs"]
    else:
        exact_programs = args.exact_programs
    exact_programs_string = " ".join(exact_programs)

    # write parameters summary file
    print("Writing parameters to parameters.txt")
    name = input_file.split('/')[-1]
    with open(f"../program_out/{name}/parameters.txt", "w") as f:
        f.write(f"{input_file=}\n{args.matrix=}\n{args.gapopen=}\n{args.gapextension=}\n{args.min_score=}\n{args.max_evalue=}\n{args.num_threads=}\n{args.num_gpus=}\n{program_list=}\n{exact_programs=}")

    # run alignment programs
    call_programs(input_file, args.matrix, args.gapopen, args.gapextension, args.min_score, args.max_evalue, args.num_threads, args.num_gpus, program_list)

    # run output parsers
    call_output_parsers(input_file, program_list)
    print("Finished parsing output.")

    subprocess.run(f"scripts/compare_results.py ../program_out/{name} ../program_out/{name}/data/{name} ../program_out/{name}/data/{name} -c {args.min_score} -v {args.max_evalue} -p {program_string} -x {exact_programs_string} {['', '-r'][args.only_runtime]}", shell=True)

 
if __name__ == '__main__':
    main()