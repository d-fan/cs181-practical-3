import sys
import csv
import pickle
import hickle as hkl
import numpy as np
from numpy import array
from sklearn.ensemble import RandomForestClassifier
from divide import folder
from conquer import sub_folder


soln_file  = 'random_forests.csv'
N = 4154804
solutions = [0] * N

with open(artists, 'r') as out:
    artists = pickle.load(out)

artist_index = {v: k for k, v in dict(enumerate(artists)).iteritems()}

for artist in artists:
    with open(folder+sub_folder+artist, 'r') as artist_fh:
        artist_csv = csv.reader(artist_fh, delimiter=',', quotechar='"')
        for row in artist_csv:
            id       = row[0]
            plays    = row[1]
            solutions[int(id) - 1] = plays


with open(soln_file, 'w') as soln_fh:
    soln_csv = csv.writer(soln_fh,
                          delimiter=',',
                          quotechar='"',
                          quoting=csv.QUOTE_MINIMAL)
    soln_csv.writerow(['Id', 'plays'])
    print 
    for id in xrange(N):
        soln_csv.writerow([id+1, solutions[id]])

