# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 22:20:10 2020

@author: Miha
"""
import tables as t

C_NAME = "Collection 1"
SAVE_LOC = "e:/Diplomska/BThesis1.h5"

class PasswordBasic(t.IsDescription):
    xhashx = t.UInt32Col()
    password = t.StringCol(64)
    #h5fisrc = t.UInt32Col()

class PasswordIntermediate(t.IsDescription):
    password = t.StringCol(64)
    length = t.UInt8Col()
    L = t.UInt8Col()
    U = t.UInt8Col()
    D = t.UInt8Col()
    S = t.UInt8Col()
    score = t.UInt8Col()
    
    


h5file = t.open_file(SAVE_LOC, mode = 'a')#, title="Database for BT")
#group = h5file.create_group("/", "C" + C_NAME[-1], C_NAME)
group = h5file.root.C1
table = h5file.create_table(group, 'f9_stats', PasswordIntermediate, "statistics", filters=t.Filters(complevel= 1, complib = 'blosc', ), expectedrows = 743106821)

#table = h5file.create_table(group, 'f9', PasswordBasic, "All the passwords (with duplicates)", filters=t.Filters(complevel= 1, complib = 'blosc', ), expectedrows = 2_700_000_000)
#index = h5file.root.C1.all_pswds.cols.xhashx.create_csindex()
table.flush()
h5file.close()



