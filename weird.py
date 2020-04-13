# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 19:39:06 2020

@author: Miha
"""

import numpy as np
import tables as t
SAVE_LOC1 = "e:/Diplomska/BThesis1.h5"
SAVE_LOC2 = "e:/Diplomska/BThesis2.h5"
stats_path = "L_ARTIFACTS.txt"

h5file_counts = t.open_file(SAVE_LOC1, mode = 'r')
h5file_stats = t.open_file(SAVE_LOC2, mode = 'r')

table_counts = h5file_counts.root.C1.f9
statsble = h5file_stats.root.C1.f9_stats
size = statsble.nrows

for i in range(21, 65):
    bumps = statsble.read_where(f"length == {i}", field="password")
    bumps_uniq, cnts = np.unique(bumps, return_counts = True)
    with open(stats_path, 'a') as file:
        resp = '\n'.join(','.join(str(j) for j in i) for i in zip(bumps_uniq, cnts))
        file.write(f"the passwords of length {i} are:\n{resp}\n")
