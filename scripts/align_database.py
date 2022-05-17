#!/usr/bin/env python3
"""Compute all-against-all protein sequence similarities of the specified database with various programs."""

import argparse
import subprocess
import os
import shutil
import sys


def call_programs(query_file, db_file, name, matrix, gapopen, gapextension, min_score, max_evalue, num_threads, num_gpus, program_list, chunk_s):
    print("Start calling of alignment programs", flush=True)
    if "blast" in program_list:
        print("Running blast...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/blast.py {query_file} {db_file} -n {name} -m {matrix} -o {gapopen} -e {gapextension} -v {max_evalue} -t {num_threads}", shell=True)
    if "mmseqs" in program_list:
        print("Running mmseqs...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/mmseqs.py {query_file} {db_file} -n {name} -m {matrix} -o {gapopen} -e {gapextension} -v {max_evalue} -t {num_threads}", shell=True)
    if "cudasw" in program_list:
        print("Running cudasw...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/cudasw.py {query_file} {db_file} -n {name} -m {matrix} -o {gapopen} -e {gapextension} -t {num_threads} -g {num_gpus} -c {min_score}", shell=True)
    if "cudasw_xargs" in program_list:
        print("Running cudasw_xargs...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/cudasw_xargs.py {query_file} {db_file} -n {name} -m {matrix} -o {gapopen} -e {gapextension} -t {num_threads} -g {num_gpus} -c {min_score} -s {chunk_s}", shell=True)
    if "ssw" in program_list:
        print("Running ssw...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/ssw.py {query_file} {db_file} -n {name} -m {matrix} -o {gapopen} -e {gapextension} -c {min_score}", shell=True)
    if "ssw_xargs" in program_list:
        print("Running ssw_xargs...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/ssw_xargs.py {query_file} {db_file} -n {name} -m {matrix} -o {gapopen} -e {gapextension} -t {num_threads} -c {min_score} -s {chunk_s}", shell=True)
    if "swipe" in program_list:
        print("Running swipe...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/swipe.py {query_file} {db_file} -n {name} -m {matrix} -o {gapopen} -e {gapextension} -t {num_threads} -c {min_score}", shell=True)
    if "swipe_xargs" in program_list:
        print("Running swipe_xargs...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/swipe_xargs.py {query_file} {db_file} -n {name} -m {matrix} -o {gapopen} -e {gapextension} -t {num_threads} -c {min_score} -s {chunk_s}", shell=True)
    if "swipe_swlib_xargs" in program_list:
        print("Running swipe_swlib_xargs...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/swipe_swlib_xargs.py {query_file} {db_file} -n {name} -m {matrix} -o {gapopen} -e {gapextension} -t {num_threads} -c {min_score} -s {chunk_s}", shell=True)
    if "water" in program_list:
        print("Running water...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/water.py {query_file} {db_file} -n {name} -m {matrix} -o {gapopen} -e {gapextension}", shell=True)
    if "adept" in program_list:
        print("Running adept...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/adept.py {query_file} {db_file} -n {name} -m {matrix} -o {gapopen} -e {gapextension} -c {min_score}", shell=True)
    if "adept_as" in program_list:
        print("Running adept_as...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/adept_as.py {query_file} {db_file} -n {name} -m {matrix} -o {gapopen} -e {gapextension} -c {min_score}", shell=True)
    if "adept_as_xargs" in program_list:
        print("Running adept_as_xargs...", flush=True)
        subprocess.run(f"/usr/bin/time scripts/program_scripts/adept_as_xargs.py {query_file} {db_file} -n {name} -m {matrix} -o {gapopen} -e {gapextension} -c {min_score} -g {num_gpus} -s {chunk_s}", shell=True)


def call_output_parsers(name, program_list):
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

    parser.add_argument("input", nargs="+",
        help="File paths of query and database files (space-separated). If only one file path is given, it will be used as query and database.")
    parser.add_argument("-n", "--name", default=None,
        help="Name of output directory. ")  
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
    parser.add_argument("-l", "--level", type=int, default=2,
        help="Level of parsing/comparing output: 2: full, 1: without comparing scores, 0: without parsing output files (only runtime comparison)")
    parser.add_argument("-s", "--chunksize", type=int, default=0,
        help="Maximal number of residues for each chunk used for xargs-scripts. If 0 (default) the chunknumber is equal to the thread/GPU number.")

    args = parser.parse_args()

    # parsing input file paths
    if len(args.input) == 1:
        ori_query_file = args.input[0]
        ori_db_file = args.input[0]
    elif len(args.input) == 2:
        ori_query_file = args.input[0]
        ori_db_file = args.input[1]
    else:
        raise Exception("Specify 1 or 2 file paths.")

    # create directory to store results, and change working directory
    name = args.name
    if name == None:
        name = f"{ori_query_file.split('/')[-1]}.{ori_db_file.split('/')[-1]}"
    print(f"Creating output directory: {os.path.abspath(f'../program_out/{name}')}")
    os.chdir(os.path.dirname(sys.path[0]))
    if os.path.exists(f"../program_out/{name}"):
        shutil.rmtree(f"../program_out/{name}")
    os.makedirs(f"../program_out/{name}/data")

    # copy input files into program_out/{name}/data
    shutil.copy(ori_query_file, f"../program_out/{name}/data/query.fasta")
    shutil.copy(ori_db_file, f"../program_out/{name}/data/db.fasta")
    # copy input files into /tmp/{name}, this is where the input files are read from the alignment programs
    if os.path.exists(f"/tmp/{name}"):
        shutil.rmtree(f"/tmp/{name}")
    os.makedirs(f"/tmp/{name}/data")
    shutil.copy(f"../program_out/{name}/data/query.fasta", f"/tmp/{name}/data/query.fasta")
    shutil.copy(f"../program_out/{name}/data/db.fasta", f"/tmp/{name}/data/db.fasta")
    query_file = f"/tmp/{name}/data/query.fasta"
    db_file = f"/tmp/{name}/data/db.fasta"

    # create program_list
    if args.programs == "all":
        program_list = ["blast", "mmseqs", "water", "ssw", "ssw_xargs", "swipe", "swipe_xargs", "swipe_swlib_xargs", "cudasw", "cudasw_xargs", "adept", "adept_as", "adept_as_xargs"]
    else:
        program_list = args.programs
    program_string = " ".join(program_list)

    # create exact_programs
    if args.exact_programs == "all":
        exact_programs = ["water", "ssw", "ssw_xargs", "swipe", "swipe_xargs", "cudasw", "cudasw_xargs", "adept", "adept_as", "adept_as_xargs"]
    else:
        exact_programs = args.exact_programs
    exact_programs_string = " ".join(exact_programs)

    # write parameters summary file
    # TODO: write original query/db name instead of query/db.fasta
    print("Writing parameters to parameters.txt")
    with open(f"../program_out/{name}/parameters.txt", "w") as f:
        f.write(f"{os.path.abspath(ori_query_file)=}\n{os.path.abspath(ori_db_file)=}\n{name=}\n{args.matrix=}\n{args.gapopen=}\n{args.gapextension=}\n{args.min_score=}\n{args.max_evalue=}\n{args.num_threads=}\n{args.num_gpus=}\n{args.chunksize=}\n{program_list=}\n{exact_programs=}\n{args.level=}")

    # prepare database
    print("Running prepare_database.py...")
    subprocess.run(f"scripts/prepare_database.py {query_file} {db_file} -t {args.num_threads} -g {args.num_gpus} -p {program_string} -s {args.chunksize}", shell=True)

    # run alignment programs
    call_programs(query_file, db_file, name, args.matrix, args.gapopen, args.gapextension, args.min_score, args.max_evalue, args.num_threads, args.num_gpus, program_list, args.chunksize)

    if args.level >= 1:
        # run output parsers
        call_output_parsers(name, program_list)
        print("Finished parsing output.")

    subprocess.run(f"scripts/compare_results.py ../program_out/{name} ../program_out/{name}/data/query.fasta ../program_out/{name}/data/db.fasta -c {args.min_score} -v {args.max_evalue} -p {program_string} -x {exact_programs_string} -l {args.level}", shell=True)

    # remove /tmp/{name}
    shutil.rmtree(f"/tmp/{name}")
 
if __name__ == '__main__':
    main()