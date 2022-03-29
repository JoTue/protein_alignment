#!/usr/bin/env python3

import argparse
import pandas as pd
import numpy as np
from Bio import SeqIO
import json
import matplotlib.pyplot as plt

def compare_results(input_dir, program_list, exact_programs, query_file, db_file):
    print("Comparing results:")
    # initialize score array
    query_names, db_names = [], []
    for seq_record in SeqIO.parse(query_file, "fasta"):
        query_names.append(seq_record.name.split("|")[-1])
    for seq_record in SeqIO.parse(db_file, "fasta"):
        db_names.append(seq_record.name.split("|")[-1])
    total_alignments = len(query_names) * len(db_names)
    midx = pd.MultiIndex.from_product([program_list, query_names])
    scores = pd.DataFrame(np.full((len(midx), len(db_names)), np.nan, dtype=float), index=midx, columns=db_names) # (#programs, #queries, #db)
    # print(scores.loc[pd.IndexSlice["adept", "Y3545_CROS8"], "Y3545_CROS8"])
    
    # fill score array
    name = input_dir.split('/')[-1]
    for program in program_list:
        with open(f"{input_dir}/{program}/{name}.{program}.json") as f:
            d = json.load(f)
        for key in d:
            for value in d[key]:
                scores.loc[pd.IndexSlice[program, key], value[0]] = value[1]
    
    # check equivalence of different programs
    print("Checking equivalence of results:")
    print(f"{exact_programs=}")
    counter = 0
    for query in query_names:
        for db in db_names:
            score_vec = scores.loc[pd.IndexSlice[exact_programs, query], db]
            if not all(score == score_vec[0] for score in score_vec):
                counter += 1
                print(score_vec)
    print(f"In the results of the exact programs, there are deviations in {counter}/{total_alignments} sequence pairs.")
    
    # checking bidirectionality
    # TODO: for now only implemented for identical query/db files (symmetric matrices)
    print("Checking bidirectionality (identical scores if query/db are swapped):")
    for program in program_list:
        submatrix = scores.loc[pd.IndexSlice[program, :], :]
        print(f"{program}:\t {np.allclose(submatrix, submatrix.T)}")
            

def compare_runtime(input_dir, program_list):
    print("Runtimes of programs (in seconds):")
    runtimes = {}
    name = input_dir.split('/')[-1]
    for program in program_list:
        with open(f"{input_dir}/{program}/time.txt") as f:
            runtime = float(f.read().strip())
            runtimes[program] = runtime
            print(f"{program}:\t {runtime:.3f}")
    # plot
    runtimes_vec = [runtimes[program] for program in program_list]
    plt.bar(program_list, runtimes_vec, log=True)
    plt.ylabel('Programs')
    plt.ylabel('Runtime [sec]')
    plt.title('Runtime comparison')
    plt.savefig(f"{input_dir}/runtimes.png")
    print(f"Plot of runtime comparison saved to {input_dir}/runtimes.png")


def main():
    """ 
    Compare results of different alignment programs.
    """
    parser = argparse.ArgumentParser(description = 'Compare results of different alignment programs.')

    parser.add_argument("input",
        help="Input directory path.")
    parser.add_argument("query",
        help="Query file path.")
    parser.add_argument("db",
        help="Database file path.")
    parser.add_argument("-p", "--programs", nargs="+", default="all",
        help="List of programs to run. Default: blast, cudasw, ssw, swipe, water, adept")
    parser.add_argument("-x", "--exact-programs", nargs="+", default="all",
        help="List of programs which should yield identical results (used for checking results). Default: cudasw, ssw, swipe, water, adept")
    args = parser.parse_args()

    # create program_list
    if args.programs == "all":
        program_list = ["blast", "cudasw", "ssw", "swipe", "water", "adept", "adept_as"]
    else:
        program_list = args.programs
    # create exact_programs
    if args.exact_programs == "all":
        exact_programs = ["cudasw", "ssw", "swipe", "water", "adept", "adept_as"]
    else:
        exact_programs = args.exact_programs

    compare_results(args.input, program_list, exact_programs, args.query, args.db)
    compare_runtime(args.input, program_list)


if __name__ == '__main__':
    main()
