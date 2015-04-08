import sys
import csv
import pickle
import hickle as hkl
import numpy as np
from numpy import array
from sklearn.ensemble import RandomForestClassifier


# Predict via random forests.
def main(load=False):
    train_file = 'train.csv'
    test_file  = 'test.csv'
    soln_file  = 'random_forests.csv'
    num_trees = 10

    if not load:
        # Load the training data.
        print "parsing training data..."
        train_data = {}
        # the list of artists
        artists = []
        with open(train_file, 'r') as train_fh:
            train_csv = csv.reader(train_fh, delimiter=',', quotechar='"')
            next(train_csv, None)
            for row in train_csv:
                user   = row[0]
                artist = row[1]
                plays  = int(row[2])
            
                if not user in train_data:
                    train_data[user] = {}
                
                train_data[user][artist] = plays
                # put artist in a list
                if not artist in artists:
                    artists.append(artist)
        print "done parsing training data!"

        # number of data
        N = len(train_data)
        d = len(artists)
        # for faster access to artists
        artist_index = {v: k for k, v in dict(enumerate(artists)).iteritems()}
        # for faster access to vectors
        user_index   = {}

        # vectorize (make into matrix)
        print "vectorizing training data..."
        X_train = []
        index = 0
        for user in train_data.keys():
            prefs = train_data[user]
            vec = [0]*len(artists)
            for artist, plays in prefs.iteritems():
                vec[artist_index[artist]] = plays
            X_train.append(vec)
            # for easy access to the vector later
            user_index[user] = index
            index += 1

        # change to np array for filtering later
        X_train = array(X_train)
        print "done vectoring training data!"

        # TODO PICKLE LATER IN THE PROCESS
        print "saving data..."
        with open('user_index', "w") as out:
            pickle.dump(user_index, out)
        with open('X_train', "w") as out:
            hkl.dump(X_train, out)
        with open('artists', "w") as out:
            pickle.dump(artists, out)
        print "done saving data!"
    else:
        print "loading previous training data..."
        with open('user_index', "r") as out:
            user_index = pickle.load(out)
        with open('X_train', "r") as out:
            X_train = hkl.load(out)
        with open('artists', "r") as out:
            artists    = pickle.load(out)
        print "done loading prev training data!"


    print "training the forest..."
    # create a random forest for every artist (everybody cry)
    forests = [RandomForestClassifier(n_estimators = num_trees) for artist in artists]
    for ind in xrange(len(artists)):
        # filter for users who listened to this artist
        arr = X_train[X_train[:, ind]!= 0]
        # target vector
        t_ind = arr[:, ind]
        # delete this vector from the training data
        np.delete(arr, ind, 1)
        # train the corresponding forest
        forest = forests[ind]
        forest.fit(arr, t_ind)
    print "done training the forest."


    # make predictions 
    with open(test_file, 'r') as test_fh:
        test_csv = csv.reader(test_fh, delimiter=',', quotechar='"')
        next(test_csv, None)

        with open(soln_file, 'w') as soln_fh:
            soln_csv = csv.writer(soln_fh,
                                  delimiter=',',
                                  quotechar='"',
                                  quoting=csv.QUOTE_MINIMAL)
            soln_csv.writerow(['Id', 'plays'])

            for row in test_csv:
                id       = row[0]
                user     = row[1]
                artist   = row[2]
                user_ind = train_data[user]['index']
                art_ind  = artist_index[artist]
                
                # make sure we're not trying to fit existing pair
                user_prefs = X_train[user_ind]
                if user_prefs[art_ind] != 0:
                    pred = X_train[user_ind][art_ind]
                    print "=========MATCH FOUND ALERT ALERT ALERT EVERYONE PANIC========"
                    print "id:", id
                else:
                    # get the forest corresponding to this artist
                    forest = forests[art_ind]
                    # delete this artist's row for predicting
                    user_prefs = np.delete(user_prefs, art_ind, 1)
                    pred = forest.predict(user_prefs)

                soln_csv.writerow([id, pred])


if __name__ == "__main__":
    main("load" in sys.argv)