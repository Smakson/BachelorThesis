# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 01:37:22 2020

@author: Miha
"""

import numpy as np
import tables as t
from xxhash import xxh32_intdigest

SAVE_LOC1 = "e:/Diplomska/BThesis1.h5"
SAVE_LOC2 = "e:/Diplomska/BThesis2.h5"
stats_path = "TABLE_STATS1.txt"

h5file_counts = t.open_file(SAVE_LOC1, mode = 'r')
h5file_stats = t.open_file(SAVE_LOC2, mode = 'r')

table_counts = h5file_counts.root.C1.f9
statsble = h5file_stats.root.C1.f9_stats
size = statsble.nrows
"""
hashx, cnt = np.unique(table_counts.read(field = "xhashx", stop = size), return_counts = True)
hashx = hashx
cnt = cnt
max10cnts = np.argpartition(cnt, -10)[-10:]
max10hashes = [hashx[i] for i in max10cnts]
max10pass = []

for i in range(len(max10hashes)):
    hsh = max10hashes[i]
    valid = table_counts.read_where(f"xhashx=={hsh}", stop = size, field = "password")
    potentials, pot_cnts = np.unique(valid, return_counts = True)
    M = np.argmax(pot_cnts)
    max10pass.append((potentials[M], pot_cnts[M]))
with open(stats_path, 'a') as file:
    file.write(f"the 10 most common strings are: {','.join(max10pass)}\n")
print("Done common.")
"""
lengths, histo = np.unique(statsble.read(field='length'), return_counts = True)
print("Done lengths.")


with open(stats_path, 'a') as file:
    resp = '\n'.join(','.join(str(j) for j in i) for i in zip(lengths, histo))
    file.write(f"the length distribution is:\n{resp}\n")

scores, histo = np.unique(statsble.read(field='score'), return_counts = True)
print("Done scores.")

with open(stats_path, 'a') as file:
    resp = '\n'.join(','.join(str(j) for j in i) for i in zip(scores, histo))
    file.write(f"the score distribution is: \n{resp}\n")

lower, histo = np.unique(statsble.read(field='L'), return_counts = True)
print("Done lower.")



with open(stats_path, 'a') as file:
    resp = '\n'.join(','.join(str(j) for j in i) for i in zip(lower, histo))
    file.write(f"the lowercase characther distribution is:\n{resp}\n")

upper, histo = np.unique(statsble.read(field='U'), return_counts = True)
print("Done upper.")

with open(stats_path, 'a') as file:
    resp = '\n'.join(','.join(str(j) for j in i) for i in zip(upper, histo))
    file.write(f"the uppercase distribution is:\n{resp}\n")

digits, histo = np.unique(statsble.read(field='D'), return_counts = True)
print("Done digits.")

with open(stats_path, 'a') as file:
    resp = '\n'.join(','.join(str(j) for j in i) for i in zip(digits, histo))
    file.write(f"the digits distribution is:\n{resp}\n")
    
    
symbols, histo = np.unique(statsble.read(field='S'), return_counts = True)
print("Done symbols.")

with open(stats_path, 'a') as file:
    resp = '\n'.join(','.join(str(j) for j in i) for i in zip(symbols, histo))
    file.write(f"the score distribution is:\n{resp}\n")





"""
for i in range(1, 5):    
    iscore = [xxh32_intdigest(row['password']) for row in statsble.where(f"score=={i}")]
    hashx, cnt = np.unique(iscore, return_counts = True)
    max5cnts = np.argpartition(cnt, -5)[-5:]
    max5hashes = [hashx[i] for i in max5cnts]
    max5iscore = []
    for hsh in max5hashes:
        valid = table_counts.read_where(f"xhashx=={hsh}", stop = size, field = "password")
        potentials, pot_cnts = np.unique(valid, return_counts = True)
        M = np.argmax(pot_cnts)
        max5iscore.append((potentials[M], pot_cnts[M]))
    with open(stats_path, 'a') as file:
        file.write(f"the 5 most common passwords with a score of {i}: {','.join(str(i) for i in max5iscore)}\n")
"""