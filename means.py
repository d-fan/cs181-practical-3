import numpy as np
import csv

# Predict via the user-specific median.
# If the user has no data, use the global median.

train_file = 'train.csv'
test_file  = 'test.csv'
soln_file  = 'user_mean.csv'
sub_folder = 'solutions/'

# Load the training data.
train_data = {}
with open(train_file, 'r') as train_fh:
    train_csv = csv.reader(train_fh, delimiter=',', quotechar='"')
    next(train_csv, None)
    for row in train_csv:
        user   = row[0]
        artist = row[1]
        plays  = row[2]
    
        if not user in train_data:
            train_data[user] = {}
        
        train_data[user][artist] = int(plays)

# Compute the global mean and per-user mean.
plays_array  = []
user_means = {}
for user, user_data in train_data.iteritems():
    user_plays = []
    for artist, plays in user_data.iteritems():
        plays_array.append(plays)
        user_plays.append(plays)
 
    user_means[user] = np.mean(np.array(user_plays))
global_mean = np.mean(np.array(plays_array))

# get list of artists
with open(artists, 'r') as out:
    artists = pickle.load(out)

artist_index = {v: k for k, v in dict(enumerate(artists)).iteritems()}

# calculate the proportion of listens dedicated to this artist
for artist in artists:
    

# Write out test solutions.
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
            id     = row[0]
            user   = row[1]
            artist = row[2]

            if user in user_means:
                soln_csv.writerow([id, user_means[user]])
            else:
                print "User", id, "not in training data."
                soln_csv.writerow([id, global_mean])
                