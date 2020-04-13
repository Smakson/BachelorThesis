# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 22:04:15 2020

@author: Miha
"""

import tables as t
import numpy as np
import re
from zxcvbn import zxcvbn



def luds_parser(password):
    LUDS = 0
    D = 0
    S = 0
    L = False
    U = False
    for c in password:
        if c.islower():
            L += 1
        elif c.isupper():
            U += 1
        elif c.isdigit():
            D += 1
        elif c.isprintable():
            S += 1

    return L, U, D, S

SAVE_LOC = "e:/Diplomska/BThesis1.h5"
dumps_path = "e:/Diplomska/OTHERS/REGEX_LUDS.txt"

h5file = t.open_file(SAVE_LOC, mode = 'a')
table = h5file.root.C1.f9
new_table = h5file.root.C1.f9_stats
new_row = new_table.row

regs = [r"[a-z]+",
        r"[A-Z]+",
        r"[0-9]+",
        r"[A-Za-z]+",
        r"[a-z]+[0-9]+",
        r"[a-zA-Z]+1",
        r"[a-zA-Z]+[0-9]+",
        r"[0-9]+[a-z]+",
        r"1[a-zA-Z]+",
        r"[0-9]+[a-zA-Z]+",
        r"[a-zA-Z0-9]+",
        r"[a-zA-Z]+1!",
        r"[a-zA-Z]+!",
        r"[1!]+[a-zA-Z]+",
        r"[a-zA-Z0-9]+!"]

regs_cmpld = [re.compile(reg) for reg in regs]


def reg_matcher(password):
    return [True if reg.fullmatch(password) else False for reg in regs_cmpld]
regs_cnt = [59489859,
 1744851,
 30049483,
 66076598,
 59588025,
 9550740,
 68905245,
 7724071,
 508983,
 8506015,
 194971716,
 44009,
 127411,
 582228,
 418375]

cnt = 0

for row in table[200249305:]:
    ps = row['password'].decode(encoding='utf-8')
    new_row['password'] = row['password']
    new_row['length'] = len(ps)
    luds = luds_parser(ps)
    new_row['L'] = luds[0]
    new_row['U'] = luds[1]
    new_row['D'] = luds[2]
    new_row['S'] = luds[3]
    new_row['score'] = zxcvbn(ps)['score']
    new_row.append()
    matchs = reg_matcher(ps)
    for i in range(len(regs)):
        if matchs[i]:
            regs_cnt[i] += 1
            
    if cnt % 10**6 == 0:
        new_table.flush()

    if cnt == 10**7:
        print(f"Done {cnt}")
        cnt = 0
    cnt += 1
            

with open(dumps_path, 'a') as file:
    resp = "regex cnt is: "
    for i in range(len(regs)):
        resp += f"{regs[i]}, {regs_cnt[i]}" 
    file.write(f"regex cnt is: ")

h5file.close()