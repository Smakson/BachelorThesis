# BachelorThesis
Contains the code pertaining to my Bachelor Thesis at Ecole Polytechnique. The scripts have the following tasks:
- `init_input.py` initializes the .hd5 file with the correct objects
- `email_pass_input.py` parses the text files, filters out baddly formatted passwords and stores the good ones in the .hd5 file
- `no_dups_table.py` initially it's purpose was to eliminate duplicates, but was later refactored to just apply a statistical measurement (i.e. length, composition, score) procedure to each password and put it in a new table along with the stats.
 - `stats.py` and `average_composition.py` both measure some aggregation statistics, mostly averages.
 - `weird.py` prints out the range of lengths where anomalies occur on the lenght-frequency graph.
