import sys
import csv
import pickle
import hickle as hkl
import numpy as np
from numpy import array
from sklearn.ensemble import RandomForestClassifier

train_file = 'train.csv'
test_file  = 'test.csv'
soln_file  = 'random_forests.csv'
folder     = 'predictions/'

def sort_by_artist():
    # make predictions 
    with open(test_file, 'r') as test_fh:
        test_csv = csv.reader(test_fh, delimiter=',', quotechar='"')
        next(test_csv, None)
        for row in test_csv:
            id       = row[0]
            user     = row[1]
            artist   = row[2]
            artist_fh = open(folder + artist,'a')
            artist_csv = csv.writer(artist_fh,
                                  delimiter=',',
                                  quotechar='"',
                                  quoting=csv.QUOTE_MINIMAL)
            artist_csv.writerow([id, user, artist])

