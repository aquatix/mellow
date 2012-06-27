import sqlite3
import os
from pprint import pprint

CACHEDBVERSION = 1
CACHEDIR = os.path.join(os.environ['HOME'], '.cache/mellow')
CACHEDBFILE = 'cache.db'
#CACHEDB = os.path.join(CACHEDIR, DBFILE)


def saveArtists(artists):
	return 42



def createdb(serverInfo):
	"""
	since: 0.0.1

	This function creates new cache db files for storing lists of artists, albums etc
	"""

	#settingsdb = sqlite3.connect(SETTINGSDB)
	cachedir = os.path.join(CACHEDIR, serverInfo['username'] + '@' + serverInfo['host'])
	cachedb = sqlite3.connect(os.path.join(cachedir, CACHEDBFILE))

	cachedb.execute("CREATE TABLE cacheinfo(dbVersion INTEGER, lastartistsupdate INTEGER, lastalbumsupdate INTEGER, created INTEGER);")
	cachedb.execute("INSERT INTO cacheinfo values ({0}, {1}, {2} strftime('now'));".format(CACHEDBVERSION, 1, 1))

	cachedb.execute("CREATE TABLE artists(dbVersion INTEGER, winX INTEGER, winY INTEGER, winWidth INTEGER, winHeight INTEGER, created INTEGER);")
	cachedb.execute("CREATE TABLE albums(username STRING, password STRING, host STRING, port INTEGER, created INTEGER);")
	cachedb.execute("CREATE TABLE tracks(username STRING, password STRING, host STRING, port INTEGER, created INTEGER);")

	cachedb.commit()
	cachedb.close()

