import sys
import csv
import pickle
import hickle as hkl
import numpy as np
from numpy import array
from sklearn.ensemble import RandomForestClassifier
from divide import folder

num_trees = 10
sub_folder = 'solutions/'

# load info 
print "loading previous training data..."
with open('user_index', "r") as out:
            user_index = pickle.load(out)
with open('X_train', "r") as out:
    X_train = hkl.load(out)
with open('artists', "r") as out:
    artists    = pickle.load(out)
artist_index = {v: k for k, v in dict(enumerate(artists)).iteritems()}
print "done loading prev training data!"

# do all the predictions for a certain artst
def predict_artist(artist): 
    art_ind = artist_index[artist]
    print "training the forest..."
    # create a random forest for every artist (everybody cry)
    forest = RandomForestClassifier(n_estimators = num_trees)
    # filter for users who listened to this artist
    arr = X_train[X_train[:, art_ind]!= 0]
    # target vector
    t_ind = arr[:, art_ind]
    # delete this vector from the training data
    arr = np.delete(arr, art_ind, 1)
    forest.fit(arr, t_ind)
    print "done training the forest."
    # make predictions
    error_fh = open(folder+'errors', 'w')
    error_csv = csv.writer(error_fh,
                              delimiter=',',
                              quotechar='"',
                              quoting=csv.QUOTE_MINIMAL)
    with open(folder+sub_folder+artist, 'w') as soln_fh:
        soln_csv = csv.writer(soln_fh,
                              delimiter=',',
                              quotechar='"',
                              quoting=csv.QUOTE_MINIMAL)
        with open(folder+artist, 'r') as artist_fh:
            artist_csv = csv.reader(artist_fh, delimiter=',', quotechar='"')
            for row in artist_csv:
                id       = row[0]
                user     = row[1]
                # artist   = row[2]
                try:
                    user_ind = user_index[user]
                    # get the vector 
                    user_prefs = X_train[user_ind]
                    user_prefs = np.delete(user_prefs, art_ind)
                    pred = forest.predict(user_prefs)[0]
                    # write
                    soln_csv.writerow([id, pred])
                except KeyError:
                    error_csv.writerow([id, user, artist])
                    print "Error with :", id, user, artist
    print "done with", id, "-", artist

def predict_all():
    for artist in artists:
        predict_artist(artist)