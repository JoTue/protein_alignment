#!/usr/bin/env python3

import argparse
import pandas as pd
import numpy as np
from Bio import SeqIO
import json
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import os
import glob

def colormap(s, savename, seq1, seq2, title):
    m, n = np.shape(s)
    fig, ax = plt.subplots()
    mappable = ax.matshow(s, cmap=plt.cm.plasma, norm=LogNorm(vmin=np.nanmin(s), vmax=np.nanmax(s)))
    fig.colorbar(mappable)

    # ax.set_xticks(range(n))
    # ax.xaxis.set_ticks_position("top")
    # ax.set_xticklabels(" " + seq2, size=6)
    # ax.set_yticks(range(m))
    # ax.set_yticklabels(" " + seq1, size=6)
    
    # for i in range(m):
    #     for j in range(n):
    #         ax.text(j, i, str(s[i, j]), va="center", ha="center", size=5)
    # plt.title(title)
    plt.savefig(savename, dpi=1000)
    plt.close()


def compare_results(input_dir, program_list, exact_programs, query_file, db_file, min_score, max_evalue):
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
    # # OLD json file
    # for program in program_list:
    #     with open(f"{input_dir}/{program}/{name}.{program}.json") as f:
    #         d = json.load(f)
    #     for key in d:
    #         for value in d[key]:
    #             scores.loc[pd.IndexSlice[program, key], value[0]] = value[1]
    # NEW results file:
    for program in program_list:
        with open(f"{input_dir}/{program}/{name}.{program}.results") as f:
            for line in f:
                words = line.split()
                if words:
                    scores.loc[pd.IndexSlice[program, words[0]], words[1]] = float(words[2])
    
    # colormap
    colormap(scores.loc[pd.IndexSlice[program_list[0], :], :], f"{input_dir}/colormap.png", 0, 0, 0)
    
    # check equivalence of different programs
    print("Checking equivalence of results:")
    print(f"{exact_programs=}")
    counter = 0
    for query in query_names:
        for db in db_names:
            score_vec = scores.loc[pd.IndexSlice[exact_programs, query], db]
            if not all(score == score_vec[0] for score in score_vec):
                for score in score_vec:
                    if score > min_score:
                        counter += 1
                        print(score_vec)
                        break
    print(f"In the results of the exact programs, there are deviations in {counter}/{total_alignments} sequence pairs.")
    
    # checking bidirectionality for identical query/db files (symmetric matrices)
    if query_names == db_names:
        print("Checking bidirectionality (identical scores if query/db are swapped):")
        for program in program_list:
            submatrix = scores.loc[pd.IndexSlice[program, :], :]
            print(f"{program}:\t {np.allclose(submatrix, submatrix.T, equal_nan=True)}")

    # checking sensitivity of heuristics
    print(f"Checking sensitivity of heuristics:\n{min_score=}\n{max_evalue=}")
    exact_program = exact_programs[0]
    heuristics = list(set(program_list).intersection(set(["blast", "mmseqs"])))
    sensitivity_df = pd.DataFrame(np.zeros((3, len(heuristics)+1), dtype=int), index=["total_ali", "high_score_ali", "high_score_hit"], columns=["SW"]+heuristics)
    sensitivity_df["SW"]["total_ali"] = total_alignments

    for query in query_names:
        for db in db_names:
            exact_score = scores.loc[pd.IndexSlice[exact_program, query], db]
            if exact_score >= min_score:
                sensitivity_df["SW"]["high_score_ali"] += 1
                sensitivity_df["SW"]["high_score_hit"] += 1
            for heuristic in heuristics:
                heuristic_score = scores.loc[pd.IndexSlice[heuristic, query], db]
                if not np.isnan(heuristic_score):
                    sensitivity_df[heuristic]["total_ali"] += 1
                    if heuristic_score >= min_score:
                        # if exact_score < min_score:
                        #     raise ValueError
                        sensitivity_df[heuristic]["high_score_ali"] += 1
                    if exact_score >= min_score:
                        sensitivity_df[heuristic]["high_score_hit"] += 1
    print(sensitivity_df)
            

def compare_runtime(input_dir, program_list):
    print("Runtimes of programs (in seconds):")
    runtimes = {}
    name = input_dir.split('/')[-1]
    with open(f"{input_dir}/time.txt", "w") as out_f:
        for program in program_list:
            with open(f"{input_dir}/{program}/time.txt") as f:
                runtime = float(f.read().strip())
                runtimes[program] = runtime
                print(f"{str(program+':').ljust(20)}{runtime:.3f}")
                out_f.write(f"{str(program+':').ljust(20)}{runtime:.3f}\n")
    # plot
    runtimes_vec = [runtimes[program] for program in program_list]
    plt.rcParams["figure.figsize"] = (len(program_list)*0.7, 5)
    plt.bar(program_list, runtimes_vec, log=True)
    plt.ylabel('Runtime [sec]')
    plt.title('Runtime comparison')
    plt.xticks(fontsize=9, rotation='vertical')
    # write times as labels on top of each bar
    # y_offset = max(runtimes_vec)/100
    for i in range(len(program_list)):
        plt.text(i, runtimes_vec[i]+(runtimes_vec[i]/30), f'{runtimes_vec[i]:.0f}', ha='center', fontsize=7)
    plt.savefig(f"{input_dir}/runtimes.png", bbox_inches="tight")
    plt.close()
    print(f"Plot of runtime comparison was created.")


def compare_cpu_usage(input_dir, program_list):
    cpu_usages = {}
    with open(f"{input_dir}/cpu_usage.txt") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            program, cpu_usage = line.split(":")
            cpu_usage = int(cpu_usage.strip())
            cpu_usages[program] = cpu_usage
    # plot
    cpu_usage_vec = [cpu_usages[program] for program in program_list]
    plt.rcParams["figure.figsize"] = (len(program_list)*0.7, 5)
    plt.bar(program_list, cpu_usage_vec)
    plt.ylabel('CPU usage [%]')
    plt.title('CPU usage comparison')
    plt.xticks(fontsize=9, rotation='vertical')
    # write CPU usage as labels on top of each bar
    # y_offset = max(runtimes_vec)/100
    for i in range(len(program_list)):
        plt.text(i, cpu_usage_vec[i]+max(cpu_usage_vec)/100, f'{cpu_usage_vec[i]:.0f}', ha='center', fontsize=7)
    plt.savefig(f"{input_dir}/cpu_usage.png", bbox_inches="tight")
    plt.close()
    print(f"Plot of CPU usage comparison was created.")


def check_json_file_sizes(input_dir, program_list):
    # for OLD json file, not needed anymore
    sizes = []
    used_programs = []
    for program in ["cudasw", "cudasw_xargs", "ssw", "ssw_xargs", "swipe", "swipe_xargs", "adept", "adept_as", "adept_as_xargs"]: # not water
        if program in program_list:
            used_programs.append(program)
            fn = glob.glob(f"{input_dir}/{program}/*.json")[0]
            sizes.append(os.path.getsize(fn))
    if all(s==sizes[0] for s in sizes):
        print("All json files of the exact programs with min_score parameter are of identical size.")
    else:
        print("NOT all json files of the exact programs with min_score parameter are of identical size. File sizes:")
        print([x for x in zip(used_programs, sizes)])


def check_results_file_sizes(input_dir, program_list):
    sizes = []
    used_programs = []
    for program in ["cudasw", "cudasw_xargs", "ssw", "ssw_xargs", "swipe", "swipe_xargs", "adept", "adept_as", "adept_as_xargs"]: # not water
        if program in program_list:
            used_programs.append(program)
            fn = glob.glob(f"{input_dir}/{program}/*.results")[0]
            sizes.append(os.path.getsize(fn))
    if all(s==sizes[0] for s in sizes):
        print("All results files of the exact programs with min_score parameter are of identical size.")
    else:
        print("NOT all results files of the exact programs with min_score parameter are of identical size. File sizes:")
        print([x for x in zip(used_programs, sizes)])


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
    parser.add_argument("-c", "--min-score", type=int, default=50,
        help="Minimimum score of alignments to show.")
    parser.add_argument("-v", "--max-evalue", type=int, default=20,
        help="Maximum e-value.")
    parser.add_argument("-p", "--programs", nargs="+", default="all",
        help="List of programs to run. Default: all")
    parser.add_argument("-x", "--exact-programs", nargs="+", default="all",
        help="List of programs which should yield identical results (used for checking results). Default: all SW implementations")
    parser.add_argument("-l", "--level", type=int, default=2,
        help="Level of parsing/comparing output: 2: full, 1: without comparing scores, 0: without parsing output files (only runtime comparison)")
    parser.add_argument("--cpu-usage", action='store_true',
        help="If set, compares CPU usage (only possible if called within a SLURM job)")

    args = parser.parse_args()

    # create program_list
    if args.programs == "all":
        program_list = ["blast", "mmseqs", "water", "ssw", "ssw_xargs", "swipe", "swipe_xargs", "swipe_swlib_xargs", "cudasw", "cudasw_xargs", "adept", "adept_as", "adept_as_xargs"]
    else:
        program_list = args.programs
    # create exact_programs
    if args.exact_programs == "all":
        exact_programs = ["cudasw", "cudasw_xargs", "ssw", "ssw_xargs", "swipe", "swipe_xargs", "water", "adept", "adept_as", "adept_as_xargs"]
    else:
        exact_programs = args.exact_programs

    compare_runtime(args.input, program_list)
    if args.cpu_usage:
        compare_cpu_usage(args.input, program_list)
    if args.level >= 1:
        check_results_file_sizes(args.input, program_list)
    if args.level >= 2:
        compare_results(args.input, program_list, exact_programs, args.query, args.db, args.min_score, args.max_evalue)


if __name__ == '__main__':
    main()
