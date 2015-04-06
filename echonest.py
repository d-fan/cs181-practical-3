#!/usr/bin/python

import pickle
import requests
import atexit

# This will scrape data with the Echo Nest API
# 

# Available buckets are (http://developer.echonest.com/docs/v4/artist.html):
avail_buckets = [
	'biographies',
	'blogs',
	'discovery',
	'discovery_rank',
	'doc_counts',
	'familiarity',
	'familiarity_rank',
	'genre',
	'hotttnesss',
	'hotttnesss_rank',
	'images',
	'artist_location',
	'news',
	'reviews',
	'songs',
	'urls',
	'video',
	'years_active'
]

# Cache queries
artist_data = {}
try:
	cachefile = open("echonest.cache", "r")
	artist_data = pickle.load(cachefile)
	cachefile.close()
except:
	# We'll create the cache file later
	pass

# Make a pickle dump, and register callback to run this on exit
def save_cache():
	with open("echonest.cache", "w") as cachefile:
		pickle.dump(artist_data, cachefile)
atexit.register(save_cache)

# Pass in an artist name (string) and a list of information to query (list of strings). This will return a dictionary of the response,
# e.g. echonest.get('weezer') will return a dict with 
def get(name, buckets=avail_buckets):
	global artist_data
	name = name.lower()
	print name in artist_data

	if name in artist_data and all([b in artist_data[name] or (b+'s') in artist_data[name] for b in buckets]):
		print "using cached value"
		return artist_data[name]
	
	# Construct GET request
	parts = [
		'http://developer.echonest.com/api/v4/artist/profile',
		'?name=%s' % name,
		'&api_key=SBUU9O8LMHSWS8Y9B',
		"".join(["&bucket=%s" % b for b in buckets])
	]
	url = "".join(parts)
	print url

	# Retrieve and add to cache
	result = requests.get(url)
	artist = result.json()['response']['artist']
	artist_data.update({artist['name'].lower(): artist})
	return artist
