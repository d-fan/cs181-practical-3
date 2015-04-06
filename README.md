# cs181-practical-3
CS 181 practical

## Tools
### echonest.py

This allows you to query Echo Nest for artist information. See http://developer.echonest.com/docs/v4/artist.html for sample return formats. 
  ```python
  import echonest
  echonest.get('lorde', ['genre'])
  ```
Will return
  ```python
  {u'genres': [{u'name': u'metropopolis'}, {u'name': u'pop'}],
  u'id': u'ARUXAKW13D610B0A9B',
  u'name': u'Lorde'}
  ```
Available queries are
- `biographies`	returns up to the 15 most recent biographies found on the web related to the artist
- `blogs`	returns up to the 15 most recent blogs found on the web related to the artist
- `discovery`	returns the discovery score for the artist. This is a measure of how unexpectedly popular the artist is.
- `discovery_rank`	returns the discovery rank for the artist
- `doc_counts`	returns document counts for each of the various artist document types
- `familiarity`	returns the familiarity for the artist
- `familiarity_rank`	returns the familiarity rank for the artist
- `genre`	returns all genres for an artist
- `hotttnesss`	returns the hotttnesss for the artist
- `hotttnesss_rank`	returns the hotttnesss rank for the artist
- `images`	returns up to the 15 most recent images found on the web related to the artist
- `artist_location`	returns information about the location of origin for the artist
- `news`	returns up to the 15 most recent news articles found on the web related to the artist
- `reviews`	returns up to the 15 most recent reviews found on the web related to the artist
- `songs`	returns up to the 15 hotttest songs for the artist
- `urls`	returns links to this artist's pages on various sites
- `video`	returns up to the 15 most recent videos found on the web related to the artist
- `years_active`	returns years active information for the artist
