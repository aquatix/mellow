import sqlite3
import os
from pprint import pprint

CACHEDBVERSION = 1
CACHEDIR = os.path.join(os.environ['HOME'], '.cache/mellow')
CACHEDBFILE = 'cache.sqlite'
#CACHEDB = os.path.join(CACHEDIR, CACHEDBFILE)


def haveCachedArtists(serverInfo):
	cachedir = initCache(serverInfo)

	cachedb = sqlite3.connect(os.path.join(cachedir, CACHEDBFILE))
	dbcursor = cachedb.cursor()
	dbcursor.execute("SELECT count(*) from artists;")
	numberOfCachedArtists = dbcursor.fetchone()

	if 0 == numberOfCachedArtists[0]:
		return False
	else:
		return True


def clearArtists(serverInfo):
	"""
	Deletes the artist cache
	"""
	cachedir = initCache(serverInfo)

	cachedb = sqlite3.connect(os.path.join(cachedir, CACHEDBFILE))
	dbcursor = cachedb.cursor()
	dbcursor.execute("DELETE from artists;")
	cachedb.commit()


def getArtists(serverInfo):
	"""
	Get the list of artists from the cache
	"""
	cachedir = initCache(serverInfo)

	artists = []

	cachedb = sqlite3.connect(os.path.join(cachedir, CACHEDBFILE))
	dbcursor = cachedb.cursor()
	for currentArtist in dbcursor.execute("SELECT * from artists;"):
		print(currentArtist)
		if None != currentArtist:
			artists.append({'id': currentArtist[0], 'name': str(currentArtist[1]), 'indexLetter': currentArtist[2]})

	print('the artists: ')
	pprint(artists)
	return artists



def saveArtists(serverInfo, artists):
	"""
	Save the list of artists to cache for easy and fast querying
	"""

	theArtists = []

	#for artistLetter in artists['indexes']['index']:
	for artistLetter in artists['index']:
		theseArtists = artistLetter['artist']
		thisLetter = artistLetter['name']

		if type(theseArtists) == "dictionary'):
			theseArtists = [theseArtists]

		for thisArtist in theseArtists:
			pprint(theseArtists)
			pprint(thisArtist)
			coverArt = ""
			try:
				coverArt = thisArtist['coverArt']
			except KeyError, e:
				coverArt = ""
			theArtists.append([thisArtist['id'], thisArtist['name'], coverArt, thisArtist['albumCount'], thisLetter])

	cachedir = initCache(serverInfo)

	cachedb = sqlite3.connect(os.path.join(cachedir, CACHEDBFILE))
	dbcursor = cachedb.cursor()
	dbcursor.executemany('INSERT INTO artists VALUES (?,?,?,?,?)', theArtists)
	cachedb.commit()
	cachedb.close()

	# Larger example that inserts many records at a time
	#purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
	#	     ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
	#	     ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
	#	    ]
	#c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

	#return theArtists.count()
	return True


def clearAlbums(serverInfo):
	"""
	Deletes the album cache
	"""
	cachedir = initCache(serverInfo)

	cachedb = sqlite3.connect(os.path.join(cachedir, CACHEDBFILE))
	dbcursor = cachedb.cursor()
	dbcursor.execute("DELETE from albums;")
	cachedb.commit()


def getAlbums(serverInfo, artistID):
	"""
	Get the list of albums of a certain artist from the cache
	albums(albumID INTEGER, name STRING, coverArt STRING, songCount INTEGER, duration INTEGER, artist STRING, artistID INTEGER, created STRING);")

	"""
	cachedir = initCache(serverInfo)

	albums = []

	print('getting albums for artist ?', artistID)

	cachedb = sqlite3.connect(os.path.join(cachedir, CACHEDBFILE))
	dbcursor = cachedb.cursor()
	
	filter = ''
	if -1 < artistID:
		filter = ' WHERE artistID=' + str(artistID)

	#for currentAlbum in dbcursor.execute("SELECT * from albums WHERE artistID=?;", (artistID, )):
	for currentAlbum in dbcursor.execute("SELECT * from albums" + filter):
		#print(currentArtist)
		if None != currentAlbum:
			albums.append({'id': currentAlbum[0], 'name': str(currentAlbum[1]), 'coverArt':str(currentAlbum[2]), 'songCount':currentAlbum[3], 'duration':currentAlbum[4], 'artist': currentAlbum[5], 'artistID':currentAlbum[6], 'created':currentAlbum[7]})

	#pprint(artists)

	return albums


def saveAlbums(serverInfo, albums):
	"""
	Save the list of albums to cache for easy and fast querying
	                 {u'artist': u'Abney Park',
                         u'artistId': 80,
                         u'coverArt': u'al-191',
                         u'created': u'2009-08-08T11:59:03',
                         u'duration': 2552,
                         u'id': 191,
                         u'name': u'From Dreams or Angels',
                         u'songCount': 11},
	"""

	theAlbums = []

	print("caching ? albums", albums['albumCount'])
	if 1 == albums['albumCount']:
		# Only one album, fix the list:
		albums["album"] = [albums["album"]]

	#print("multiple albums")
	#print albums['album'].count()
	#pprint(albums)
	for thisAlbum in albums["album"]:
		#pprint(thisAlbum)
		coverArt = ""
		try:
			coverArt = thisAlbum['coverArt']
		except KeyError, e:
			coverArt = ""
		# albums(albumID INTEGER, parentID INTEGER, album STRING, title STRING, artist STRING, isDir BOOLEAN, coverart INTEGER, created STRING);
		# albums(albumID INTEGER, name STRING, coverart STRING, songcount INTEGER, duration INTEGER, artist STRING, artistID INTEGER, created STRING);")
		theAlbums.append([thisAlbum['id'], thisAlbum['name'], coverArt, thisAlbum['songCount'], thisAlbum['duration'], thisAlbum['artist'], thisAlbum['artistId'], thisAlbum['created']])

	cachedir = initCache(serverInfo)

	cachedb = sqlite3.connect(os.path.join(cachedir, CACHEDBFILE))
	#dbcursor = cachedb.cursor()
	#dbcursor.executemany('INSERT INTO albums VALUES (?,?,?,?,?,?,?,?)', theAlbums)
	cachedb.executemany('INSERT INTO albums VALUES (?,?,?,?,?,?,?,?)', theAlbums)
	cachedb.commit()
	cachedb.close()

	return True


def clearTracks(serverInfo):
	"""
	Deletes the album/track cache
	"""
	cachedir = initCache(serverInfo)

	cachedb = sqlite3.connect(os.path.join(cachedir, CACHEDBFILE))
	dbcursor = cachedb.cursor()
	dbcursor.execute("DELETE from tracks;")
	cachedb.commit()


def getTracks(serverInfo, artistID, albumID):
	"""
	Get the list of artists from the cache
	tracks(trackID INTEGER, albumID INTEGER, parentID INTEGER, album STRING, title STRING, artist STRING, artistID INTEGER, genre STRING, year INTEGER, type STRING, contentType STRING, duration INTEGER, bitrate INTEGER, size INTEGER, isVideo BOOLEAN, path STRING, suffix STRING, created STRING);

	"""
	cachedir = initCache(serverInfo)

	tracks = []
	
	tracksFilter = ''
	
	if -1 < artistID:
		# Filter on artist
		tracksFilter = tracksFilter + ' artistID=' + str(artistID)
	if -1 < albumID:
		# Filter on album
		if 0 < tracksFilter.length:
			tracksFilter = tracksFilter + ' AND '
		tracksFilter = tracksFilter + ' albumID=' + str(albumID)

	if 0 < tracksFilter.length:
		tracksFilter = ' WHERE ' + tracksFilter

	cachedb = sqlite3.connect(os.path.join(cachedir, CACHEDBFILE))
	dbcursor = cachedb.cursor()
	for currentTrack in dbcursor.execute("SELECT * from tracks " + tracksFilter):
		#print(currentArtist)
		if None != currentTrack:
			tracks.append({'id': currentTrack[0], 'name': str(currentTrack[1]), 'indexLetter': currentTrack[2]})

	return tracks


def saveTracks(serverInfo, tracks):
	"""
	Save the list of tracks to cache for easy and fast querying
	tracks(trackID INTEGER, albumID INTEGER, parentID INTEGER, album STRING, title STRING, artist STRING, artistID INTEGER, genre STRING, year INTEGER, type STRING, contentType STRING, duration INTEGER, bitrate INTEGER, size INTEGER, isVideo BOOLEAN, path STRING, suffix STRING, created STRING);

	"""

	theTracks = []

	#for artistLetter in artists['indexes']['index']:
	for artistLetter in artists['index']:
		theseArtists = artistLetter['artist']
		thisLetter = artistLetter['name']

		for thisArtist in theseArtists:
			theArtists.append([thisArtist['id'], thisArtist['name'], thisLetter])

	cachedir = initCache(serverInfo)

	cachedb = sqlite3.connect(os.path.join(cachedir, CACHEDBFILE))
	dbcursor = cachedb.cursor()
	dbcursor.executemany('INSERT INTO artists VALUES (?,?,?)', theArtists)
	cachedb.commit()
	cachedb.close()

	return True




# == Utility functions ======

def getCacheDir(serverInfo):
	"""
	Generate the cache dir from the server info
	Looks like ~/.cache/mellow/USER@SERVER/cache.db
	"""
	hostname = serverInfo['host']
	hostname = hostname.replace('https', '').replace('http', '').replace('://', '')
	cachedir = os.path.join(CACHEDIR, serverInfo['username'] + '@' + hostname)
	return cachedir


def initCache(serverInfo):
	"""
	Create ~/.cache/mellow/USER@SERVER/cache.db if it does not exist yet
	"""

	cachedir = getCacheDir(serverInfo)

	if os.path.isfile(os.path.join(cachedir, CACHEDBFILE)):
		cachedb = sqlite3.connect(os.path.join(cachedir, CACHEDBFILE))
		dbcursor = cachedb.cursor()
		dbcursor.execute("SELECT dbVersion from cacheinfo;")
		cacheVersion = dbcursor.fetchone()

		if CACHEDBVERSION != cacheVersion[0]:
			# CacheDB version has changed, delete old cache file as it's incompatible
			print("Removing old cache file {} with version {} as version {} is needed".format(os.path.join(cachedir, CACHEDBFILE), cacheVersion[0], CACHEDBVERSION))
			os.remove(os.path.join(cachedir, CACHEDBFILE))

	# Check whether the settings db exists, create if not
	if not os.path.isdir(cachedir):
		os.makedirs(cachedir)
	if not os.path.isfile(os.path.join(cachedir, CACHEDBFILE)):
		createdb(serverInfo)

	return cachedir


def createdb(serverInfo):
	"""
	since: 0.0.1

	This function creates new cache db files for storing lists of artists, albums etc
	"""

	cachedir = getCacheDir(serverInfo)
	cachedb = sqlite3.connect(os.path.join(cachedir, CACHEDBFILE))

	cachedb.execute("CREATE TABLE cacheinfo(dbVersion INTEGER, lastartistsupdate INTEGER, lastalbumsupdate INTEGER, created INTEGER);")
	cachedb.execute("INSERT INTO cacheinfo values ({0}, {1}, {2}, strftime('now'));".format(CACHEDBVERSION, 1, 1))

	cachedb.execute("CREATE TABLE artists(artistID INTEGER, name STRING, coverArt STRING, albumCount INTEGER, indexLetter STRING);")
	cachedb.execute("CREATE INDEX artist_id ON artists(artistID);")
	
	cachedb.execute("CREATE TABLE albums(albumID INTEGER, name STRING, coverArt STRING, songCount INTEGER, duration INTEGER, artist STRING, artistID INTEGER, created STRING);")
	cachedb.execute("CREATE INDEX album_id ON albums(albumID);")
	cachedb.execute("CREATE INDEX albumartist_id ON albums(artistID);")
	
	cachedb.execute("CREATE TABLE tracks(trackID INTEGER, albumID INTEGER, parentID INTEGER, album STRING, title STRING, artist STRING, artistID INTEGER, genre STRING, year INTEGER, type STRING, contentType STRING, duration INTEGER, bitrate INTEGER, size INTEGER, isVideo BOOLEAN, path STRING, suffix STRING, created STRING);")
	cachedb.execute("CREATE INDEX track_id ON tracks(trackID);")

	cachedb.commit()
	cachedb.close()

