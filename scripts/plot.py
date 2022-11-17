#!/usr/bin/env python3

import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_vary_scoring(input_file, figname):
    """b.sh"""
    PROGRAMS = ["SSW", "SWIPE", "CUDASW", "ADEPT"]  # same order as in input_file
    d = {}
    # parse runtimes
    with open(input_file) as f:
        line = f.readline()
        while line:
            if line.startswith("Creating temporary directory:"):
                header = line.split("/")[-1]
                _, matrix, gapo, gape = header.strip().split("_")
                if matrix not in d:
                    d[matrix] = {(gapo, gape): []}
                else:
                    d[matrix][(gapo, gape)] = []
            if line.startswith("Runtimes of programs"):
                line = f.readline()
                while not line.startswith("Plot of runtime comparison was created."):
                    d[matrix][(gapo, gape)].append(float(line.split()[-1]))
                    line = f.readline()
            line = f.readline()
    # plot
    for matrix in d:
        gap_penalties = list(d[matrix].keys())
        gap_penalties = [f"{tup[0]}/{tup[1]}" for tup in gap_penalties]
        for i in range(len(PROGRAMS)):
            plt.plot(gap_penalties, [d[matrix][gap_penalty][i] for gap_penalty in d[matrix]], label=PROGRAMS[i])
        plt.legend()
        plt.title(matrix)
        plt.xlabel("Gap open / Gap extension penalties")
        plt.ylabel("Runtime [sec]")
        plt.yscale('log')
        plt.ylim(100, 7000)
        plt.savefig(f"/scratch/cube/tuechler/protein_alignment/analysis/{figname}_{matrix}.png")
        plt.close()

def plot_vary_query_db_size(input_file, figname):
    """a4.sh"""
    PROGRAMS = ["SSW", "SWIPE", "CUDASW", "ADEPT"]  # same order as in input_file
    d = {}
    # parse runtimes
    with open(input_file) as f:
        line = f.readline()
        while line:
            if line.startswith("Creating temporary directory:"):
                header = line.split("/")[-1]
                _, query, db = header.strip().split("_")
                d[(query, db)] = []
            if line.startswith("Runtimes of programs"):
                line = f.readline()
                while not line.startswith("Plot of runtime comparison was created."):
                    d[(query, db)].append(float(line.split()[-1]))
                    line = f.readline()
            line = f.readline()
    # plot
    sizes = list(d.keys())
    sizes = [f"$2^{{{int(tup[0])}}}$/$2^{{{int(tup[1])}}}$" for tup in sizes]
    for i in range(len(PROGRAMS)):
        plt.plot(sizes, [d[size][i] for size in d], label=PROGRAMS[i])
    plt.legend()
    plt.title("Varying matrix dimensions")
    plt.xlabel("Query / Db sizes [number of sequences]")
    plt.ylabel("Runtime [sec]")
    plt.yscale('log')
    plt.savefig(f"/scratch/cube/tuechler/protein_alignment/analysis/{figname}.png")
    plt.close()


def plot_vary_seqlengths(input_file, figname):
    """c.sh
    fixed query seqlengths per plot"""
    PROGRAMS = ["SSW", "SWIPE", "CUDASW", "ADEPT"]  # same order as in input_file
    d = {}
    # parse runtimes
    with open(input_file) as f:
        line = f.readline()
        while line:
            if line.startswith("Creating temporary directory:"):
                header = line.split("/")[-1]
                _, _, _, query_min, query_max, _, _, db_min, db_max = header.strip().split("_")
                if (query_min, query_max) not in d:
                    d[(query_min, query_max)] = {(db_min, db_max): []}
                else:
                    d[(query_min, query_max)][(db_min, db_max)] = []
            if line.startswith("Runtimes of programs"):
                line = f.readline()
                while not line.startswith("Plot of runtime comparison was created."):
                    d[(query_min, query_max)][(db_min, db_max)].append(float(line.split()[-1]))
                    line = f.readline()
            line = f.readline()
    # fix erroneous run
    d[('751', '1500')][('751', '1500')][-1] = np.nan
    # plot
    for query_len in d:
        query_len_print = f"{query_len[0]}-{query_len[1]}"
        db_lens = list(d[query_len].keys())
        db_lens = [f"{tup[0]}-{tup[1]}" for tup in db_lens]
        for i in range(len(PROGRAMS)):
            plt.plot(db_lens, [d[query_len][db_len][i] for db_len in d[query_len]], label=PROGRAMS[i])
        plt.legend()
        plt.title(f"Query sequence length range: {query_len_print}")
        plt.xlabel("Db sequence length range")
        plt.ylabel("Runtime [sec]")
        plt.yscale('log')
        plt.ylim(10, 7000)
        plt.savefig(f"/scratch/cube/tuechler/protein_alignment/analysis/{figname}_{query_len_print}.png")
        plt.close()

def main():
    """ 
    Create plots of SW performance comparisons.
    """
    parser = argparse.ArgumentParser(description = 'Create plots of SW performance comparisons.')

    parser.add_argument("input",
        help="Input file path (= SLURM output file).")
    parser.add_argument("-n", "--figname",
        help="File name of plot.")
    parser.add_argument("-i", "--index", nargs="+",
        help="List of indexes.")

    args = parser.parse_args()

    #plot_vary_scoring(args.input, args.figname)
    # plot_vary_query_db_size(args.input, args.figname)
    plot_vary_seqlengths(args.input, args.figname)

if __name__ == '__main__':
    main()
