# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 20:35:56 2020

@author: Miha
"""


import numpy as np
import tables as t
SAVE_LOC1 = "e:/Diplomska/BThesis1.h5"
SAVE_LOC2 = "e:/Diplomska/BThesis2.h5"
composition_path= "L_composition.txt"
score_path = "L_score.txt"

h5file_counts = t.open_file(SAVE_LOC1, mode = 'r')
h5file_stats = t.open_file(SAVE_LOC2, mode = 'r')

table_counts = h5file_counts.root.C1.f9
statsble = h5file_stats.root.C1.f9_stats
size = statsble.nrows

with open(score_path, 'w') as file1:
    with open(composition_path, 'w') as file2:
        for i in range(1, 20):
            print(i)
            L_avg = np.average(statsble.read_where(f"length == {i}", field="L"))
            D_avg = np.average(statsble.read_where(f"length == {i}", field="D"))
            U_avg = np.average(statsble.read_where(f"length == {i}", field="U"))
            S_avg = np.average(statsble.read_where(f"length == {i}", field="S"))
            score_avg = np.average(statsble.read_where(f"length == {i}", field="score"))
            file1.write(f"{i}, {score_avg}\n")
            file2.write(f"{i}, {L_avg}, {U_avg}, {D_avg}, {S_avg}\n")


