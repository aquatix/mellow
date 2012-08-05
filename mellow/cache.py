import sqlite3
import os
from pprint import pprint

CACHEDBVERSION = 1
CACHEDIR = os.path.join(os.environ['HOME'], '.cache/mellow')
CACHEDBFILE = 'cache.db'
#CACHEDB = os.path.join(CACHEDIR, CACHEDBFILE)


def haveCachedArtists(serverInfo):
	initCache(serverInfo)
	#if 


def saveArtists(artists):
	return 42


def getCacheDir(serverInfo):
	"""Generate the cache dir from the server info"""
	hostname = serverInfo['host']
	hostname = hostname.replace('https', '').replace('http', '').replace('://', '')
	cachedir = os.path.join(CACHEDIR, serverInfo['username'] + '@' + hostname)
	return cachedir


def initCache(serverInfo):
	"""Create ~/.cache/mellow/cache.db if it does not exist yet"""

	cachedir = getCacheDir(serverInfo)

	if os.path.isfile(os.path.join(cachedir, CACHEDBFILE)):
		cachedb = sqlite3.connect(os.path.join(cachedir, CACHEDBFILE))
		result = cachedb.execute("SELECT dbVersion from cacheinfo;")
		pprint(result)

	# Check whether the settings db exists
	if not os.path.isdir(cachedir):
		os.makedirs(cachedir)
	if not os.path.isfile(os.path.join(cachedir, CACHEDBFILE)):
		createdb(serverInfo)


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

