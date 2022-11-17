import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# # swipe_swlib_teste:
# stage_times = []
# with open("/scratch/cube/tuechler/protein_alignment/scripts/SLURM/swipe_swlib_teste-3256939.out") as f:
#     for line in f:
#         if line.startswith("time_stage1:"):
#             stage1 = float(line.split()[1])
#         elif line.startswith("time_stage2:"):
#             stage2 = float(line.split()[1])
#         elif line.startswith("time_stage3:"):
#             stage3 = float(line.split()[1])
#             stage_times.append([stage1, stage2, stage3])
# print(stage_times)
# c_values = ["45", "55", "65", "75"]

# # b50
# fig, ax = plt.subplots()
# ax.bar(c_values, [x[0] for x in stage_times[0::3]],  label='stage1', width=0.6)
# ax.bar(c_values, [x[1] for x in stage_times[0::3]],  label='stage2', bottom=[x[0] for x in stage_times[0::3]], width=0.6)
# ax.bar(c_values, [x[2] for x in stage_times[0::3]],  label='stage3', bottom=[x[0]+x[1] for x in stage_times[0::3]], width=0.6)
# ax.set_ylim(0, 3500)
# ax.set_xlabel("min_score1")
# ax.set_ylabel("Runtime [sec]")
# ax.set_title("min_score2 = 50")
# ax.legend()
# fig.savefig("/scratch/cube/tuechler/protein_alignment/analysis/sste_b50.png")

# # b65
# fig, ax = plt.subplots()
# ax.bar(c_values, [x[0] for x in stage_times[1::3]],  label='stage1', width=0.6)
# ax.bar(c_values, [x[1] for x in stage_times[1::3]],  label='stage2', bottom=[x[0] for x in stage_times[1::3]], width=0.6)
# ax.bar(c_values, [x[2] for x in stage_times[1::3]],  label='stage3', bottom=[x[0]+x[1] for x in stage_times[1::3]], width=0.6)
# ax.set_ylim(0, 3500)
# ax.set_xlabel("min_score1")
# ax.set_ylabel("Runtime [sec]")
# ax.set_title("min_score2 = 65")
# ax.legend()
# fig.savefig("/scratch/cube/tuechler/protein_alignment/analysis/sste_b65.png")

# # b80
# fig, ax = plt.subplots()
# ax.bar(c_values, [x[0] for x in stage_times[2::3]],  label='stage1', width=0.6)
# ax.bar(c_values, [x[1] for x in stage_times[2::3]],  label='stage2', bottom=[x[0] for x in stage_times[2::3]], width=0.6)
# ax.bar(c_values, [x[2] for x in stage_times[2::3]],  label='stage3', bottom=[x[0]+x[1] for x in stage_times[2::3]], width=0.6)
# ax.set_ylim(0, 3500)
# ax.set_xlabel("min_score1")
# ax.set_ylabel("Runtime [sec]")
# ax.set_title("min_score2 = 80")
# ax.legend()
# fig.savefig("/scratch/cube/tuechler/protein_alignment/analysis/sste_b80.png")


# # swipe_swlib_testc:
# # time_stage1: 277.095 s
# # time_stage2: 2109 s
# # time_stage3: 159.947 s
# stage_times = [[277.095, 2109, 159.947]]
# df = pd.DataFrame(stage_times, columns = ["stage1", "stage2", "stage3"], index=["swipe_swlib"])
# print(df)
# plot = df.plot.bar(stacked=True, width=0.4)
# fig = plot.get_figure()
# plot.set_ylabel("Runtime [sec]")
# plot.set_title("swipe_swlib\nmin_score1 = 55, minscore2 = 75")
# fig.savefig("/scratch/cube/tuechler/protein_alignment/analysis/sstc_c55b75.png", bbox_inches="tight")


# swipe_swlib_testc, hist of score (swipe):
scores = []
with open("/scratch/cube/tuechler/program_out/swipe_swlib_testc2/swipe_xargs/swipe_swlib_testc2.swipe_xargs.results") as f:
    for line in f:
        scores.append(float(line.split()[-1]))
plt.hist(scores, bins=100, range=(55, 155))
plt.title("Score distribution (BLOSUM 50/15/2)")
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.savefig("/scratch/cube/tuechler/protein_alignment/analysis/sstc_swipe_hist.png", bbox_inches="tight")


# # swipe_swlib_testh:
# from mpl_toolkits.mplot3d import Axes3D

# stage_times = np.empty((4, 12))
# with open("/scratch/cube/tuechler/protein_alignment/scripts/SLURM/sst_h-3425066.out") as f:
#     i = 0
#     for line in f:
#         if line.startswith("time_stage1:"):
#             stage1 = float(line.split()[1])
#         # elif line.startswith("time_stage2:"):
#         #     stage2 = float(line.split()[1])
#         elif line.startswith("time_stage2c:"):
#             stage2c = float(line.split()[1])
#         elif line.startswith("time_stage2d:"):
#             stage2d = float(line.split()[1])
#         elif line.startswith("time_stage3:"):
#             stage3 = float(line.split()[1])
#             stage_times[:, i] = [stage1, stage2c, stage2d, stage3]
#             i += 1

# fig = plt.figure()
# ax = fig.add_subplot(111, projection = "3d")

# ###patch start### remove axes margins
# from mpl_toolkits.mplot3d.axis3d import Axis
# if not hasattr(Axis, "_get_coord_info_old"):
#     def _get_coord_info_new(self, renderer):
#         mins, maxs, centers, deltas, tc, highs = self._get_coord_info_old(renderer)
#         mins += deltas / 4
#         maxs -= deltas / 4
#         return mins, maxs, centers, deltas, tc, highs
#     Axis._get_coord_info_old = Axis._get_coord_info  
#     Axis._get_coord_info = _get_coord_info_new
# ###patch end###

# ax.set_xlabel("-B")
# ax.set_ylabel("-c") 
# ax.set_zlabel("Runtime [sec]")
# ax.set_xlim3d(40, 90)
# ax.set_ylim3d(35, 85)
# ax.set_xticks([50, 65, 80],
#                    verticalalignment='baseline',
#                    horizontalalignment='left') 
# ax.set_yticks([45, 55, 65, 75])
# ax.set_xlim(ax.get_xlim()[::-1])
# ax.set_ylim(ax.get_ylim()[::-1])
# # ax.set_box_aspect(aspect = (0.8, 0.8, 1))

# xpos = [50, 65, 80, 50, 65, 80, 50, 65, 80, 50, 65, 80]
# ypos = [45, 45, 45, 55, 55, 55, 65, 65, 65, 75, 75, 75]
# zpos = np.zeros(12)

# width = 5
# dx = np.full(12, width)
# dy = np.full(12, width)
# dz = stage_times  # the heights of the 4 bar sets

# _zpos = zpos   # the starting zpos for each bar
# colors = ['b', 'orangered', 'orange', 'g']
# labels = ["stage 1", "stage 2 - comp.","stage 2 - alig.", "stage 3"]
# plots = []
# for i in range(4):
#     ax.bar3d([x-width//2 for x in xpos], [y-width//2 for y in ypos], _zpos, dx, dy, dz[i], color=colors[i], label=labels[i])
#     _zpos += dz[i]    # add the height of each bar to know where to start the next

# # legend
# import matplotlib.patches as mpatches
# patches = [mpatches.Patch(color=colors[i], label=labels[i]) for i in range(4)]
# plt.legend(handles=patches, loc='upper left', fontsize=7)

# plt.savefig("/scratch/cube/tuechler/protein_alignment/analysis/ssth.png", dpi=300)


# # swipe_swlib_testg2:

# # time_stage1: 336.157 s
# # time_stage2c: 750.605 s
# # time_stage2d: 1685.27 s
# # time_stage3: 183.794 s
# stage_times = [[336.157, 750.605, 1685.27, 183.794]]
# df = pd.DataFrame(stage_times, columns = ["stage 1", "stage 2 - comp.","stage 2 - alig.", "stage 3"], index=["swipe_swlib"])
# print(df)
# ax = df.plot.bar(stacked=True, width=0.3, fontsize=10, color=['b', 'orangered', 'orange', 'g'])
# fig = ax.get_figure()
# ax.set_ylabel("Runtime [sec]")
# ax.set_title("swipe_swlib\nmin_score1 = 55, minscore2 = 75")
# ax.legend(loc="upper right", fontsize=9)
# fig.savefig("/scratch/cube/tuechler/protein_alignment/analysis/sstg2_c55b75.png", bbox_inches="tight")