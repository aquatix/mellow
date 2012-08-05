import sqlite3
import os
from pprint import pprint

CACHEDBVERSION = 1
CACHEDIR = os.path.join(os.environ['HOME'], '.cache/mellow')
CACHEDBFILE = 'cache.db'
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
	for row in dbcursor.execute("SELECT * from artists;"):
		currentArtist = dbcursor.fetchone()
		#print(currentArtist)
		if None != currentArtist:
			artists.append({'id': currentArtist[0], 'name': currentArtist[1], 'indexLetter': currentArtist[2]})

	#pprint(artists)

	return artists



def saveArtists(serverInfo, artists):

	theArtists = []

	for artistLetter in artists['indexes']['index']:
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

	# Larger example that inserts many records at a time
	#purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
	#	     ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
	#	     ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
	#	    ]
	#c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

	#return theArtists.count()
	return True


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
	"""Create ~/.cache/mellow/USER@SERVER/cache.db if it does not exist yet"""

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

	#settingsdb = sqlite3.connect(SETTINGSDB)
	cachedir = getCacheDir(serverInfo)
	cachedb = sqlite3.connect(os.path.join(cachedir, CACHEDBFILE))

	cachedb.execute("CREATE TABLE cacheinfo(dbVersion INTEGER, lastartistsupdate INTEGER, lastalbumsupdate INTEGER, created INTEGER);")
	cachedb.execute("INSERT INTO cacheinfo values ({0}, {1}, {2}, strftime('now'));".format(CACHEDBVERSION, 1, 1))

	cachedb.execute("CREATE TABLE artists(artistID INTEGER, name STRING, indexLetter STRING);")
	cachedb.execute("CREATE TABLE albums(artistID INTEGER, name STRING, indexLetter STRING);")
	cachedb.execute("CREATE TABLE tracks(username STRING, password STRING, host STRING, port INTEGER, created INTEGER);")

	cachedb.commit()
	cachedb.close()

