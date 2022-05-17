# Plot output from align_database8c.sh

import matplotlib.pyplot as plt

# # dict to store times
# program_list = ["ssw", "swipe", "cudasw", "adept"]
# times = {"small_query": {"ssw": [], "swipe": [], "cudasw": [], "adept": []}, "quadratic": {"ssw": [], "swipe": [], "cudasw": [], "adept": []}}

# # read in data
# small_query_queries = ["sp_n100_10_500", "sp_n200_10_500", "sp_n400_10_500", "sp_n800_10_500", "sp_n1600_10_500", "sp_n3200_10_500"]
# for query in small_query_queries:
#     dir_name = f"{query}.sp_n40000_10_500"
#     with open(f"/scratch/cube/tuechler/program_out/{dir_name}/time.txt") as f:
#         lines = f.readlines()
#         for line in lines:
#             program, time = line.split()
#             program = program.split("_")[0]
#             time = float(time)
#             times["small_query"][program].append(time)

# quadratic_queries = ["sp_n2000_10_500", "sp_n2828_10_500", "sp_n4000_10_500", "sp_n5656_10_500", "sp_n8000_10_500", "sp_n11313_10_500"]
# for query in quadratic_queries:
#     dir_name = f"{query}.{query}"
#     with open(f"/scratch/cube/tuechler/program_out/{dir_name}/time.txt") as f:
#         lines = f.readlines()
#         for line in lines:
#             program, time = line.split()
#             program = program.split("_")[0]
#             time = float(time)
#             times["quadratic"][program].append(time)
# print(times)

# # plot
# fig, ax = plt.subplots()
# ax.set_yscale('log', base=2)
# ax.grid(True)

# x_labels = ["4M", "8M", "16M", "32M", "64M", "128M"]
# colors = ["b", "g", "r", "y", "m", "c"]
# for i, program in enumerate(times["small_query"]):
#     ax.plot(x_labels, times["small_query"][program],
#             marker='o', linewidth=2, label=program, c=colors[i])
#     ax.plot(x_labels, times["quadratic"][program],
#             marker='x', linewidth=2, label=program, c=colors[i])
# ax.set_xlabel('#alignments')
# ax.set_ylabel('runtime [sec]')
# ax.set_title("Runtimes: small query vs. quadratic matrix")

# #https://stackoverflow.com/questions/45140295/how-to-create-a-legend-of-both-color-and-marker
# markers=["o", "x"]
# f = lambda m,c: plt.plot([],[],marker=m, color=c, ls="none")[0]
# handles = [f(markers[i], "k") for i in range(len(markers))]
# handles += [f("s", colors[i]) for i in range(len(program_list))]
# labels =  ["small_query", "quadratic"] + program_list
# plt.legend(handles, labels)

# plt.savefig("/scratch/cube/tuechler/protein_alignment/analysis/small_query_vs_quadratic.png")

# PLOT 2
# dict to store times
program_list = ["ssw", "swipe", "cudasw", "adept"]
times = {"ssw": [], "swipe": [], "cudasw": [], "adept": []}

# read in data
databases = ["sp_n1000_10_500", "sp_n4000_10_500", "sp_n16000_10_500", "sp_n64000_10_500"] #, "sp_n256000_10_500"
for db in databases:
    dir_name = f"sp_n1000_10_500.{db}"
    with open(f"/scratch/cube/tuechler/program_out/{dir_name}/time.txt") as f:
        lines = f.readlines()
        for line in lines:
            program, time = line.split()
            program = program.split("_")[0]
            time = float(time)
            times[program].append(time)

# TODO remove:
times["ssw"].append(2785)
times["swipe"].append(4181)
times["cudasw"].append(202)
times["adept"].append(3724)
print(times)

# plot
fig, ax = plt.subplots()
ax.set_yscale('log', base=2)
ax.grid(True)

x_labels = ["1K", "4K", "16K", "64K", "256K"]
colors = ["b", "g", "r", "y", "m", "c"]
for i, program in enumerate(times):
    ax.plot(x_labels, times[program],
            marker='o', linewidth=2, label=program, c=colors[i])
ax.set_xlabel('Database size')
ax.set_ylabel('Runtime [sec]')
ax.set_title("Runtimes: 1K query vs. various database sizes")

plt.legend()

plt.savefig("/scratch/cube/tuechler/protein_alignment/analysis/fixed_query.png")

# PLOT 3

# dict to store times
program_list = ["ssw", "swipe", "cudasw", "adept"]
times = {"small_query": {"ssw": [], "swipe": [], "cudasw": [], "adept": []}, "quadratic": {"ssw": [], "swipe": [], "cudasw": [], "adept": []}}

# read in data
small_query_queries = ["sp_n100_10_500", "sp_n200_10_500", "sp_n400_10_500", "sp_n800_10_500", "sp_n1600_10_500", "sp_n3200_10_500"]
for query in small_query_queries:
    dir_name = f"{query}.sp_n40000_10_500"
    with open(f"/scratch/cube/tuechler/program_out/{dir_name}/time.txt") as f:
        lines = f.readlines()
        for line in lines:
            program, time = line.split()
            program = program[:program.rindex("_")]
            time = float(time)
            times["small_query"][program].append(time)

quadratic_queries = ["sp_n2000_10_500", "sp_n2828_10_500", "sp_n4000_10_500", "sp_n5656_10_500", "sp_n8000_10_500", "sp_n11313_10_500"]
for query in quadratic_queries:
    dir_name = f"{query}.{query}"
    with open(f"/scratch/cube/tuechler/program_out/{dir_name}/time.txt") as f:
        lines = f.readlines()
        for line in lines:
            program, time = line.split()
            program = program.split("_")[0]
            time = float(time)
            times["quadratic"][program].append(time)
print(times)

# plot
fig, ax = plt.subplots()
ax.set_yscale('log', base=2)
ax.grid(True)

x_labels = ["100", "200", "400", "800", "1600", "3200"]
colors = ["b", "g", "r", "y", "m", "c"]
for i, program in enumerate(times["small_query"]):
    ax.plot(x_labels, times["small_query"][program],
            marker='o', linewidth=2, label=program, c=colors[i])
ax.set_xlabel('Query size')
ax.set_ylabel('Runtime [sec]')
ax.set_title("Runtimes: various query sizes vs. 40K database")

plt.legend()

plt.savefig("/scratch/cube/tuechler/protein_alignment/analysis/fixed_database.png")