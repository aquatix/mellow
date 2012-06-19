import sqlite3
import os
from pprint import pprint

#print(sqlite3.version_info)
#print(sqlite3.sqlite_version_info)
#print(sqlite3.__file__)

DBVERSION = 1
DBDIR = os.path.join(os.environ['HOME'], '.config/mellow')
DBFILE = 'mellow.db'
SETTINGSDB = os.path.join(DBDIR, DBFILE)


def settings():
	"""
	Fetches the app settings, create the settings dir and file if not existing yet

	~/.config/mellow/mellow.db
	"""

	# Check whether the settings db exists
	if not os.path.isdir(DBDIR):
		os.makedirs(DBDIR)
	if not os.path.isfile(DBFILE):
		self.createdb()


	settingsdb = sqlite3.connect(SETTINGSDB)
	for row in settingsdb.execute('SELECT dbVersion, winX, winY, winWidth, winHeight, created FROM settingsinfo'):
		print(row)
		settingsinfo = {'dbVersion': row[0], 'winX': row[1], 'winY': row[2], 'winWidth': row[3], 'winHeight': row[4], 'created': row[5]}
		return settingsinfo


def login():
	"""
	since: 0.0.1

	This function logs the application into the remote Subsonic server
	"""

	settingsdb = sqlite3.connect(SETTINGSDB)

	# for the time, default to 'michiel'
	username = ('michiel',)

	for row in settingsdb.execute('SELECT username, password, host, port, created FROM userinfo WHERE username=?', username):
		#print(row)
		userinfo = {'username': row[0], 'password': row[1], 'host': row[2], 'port': row[3], 'created': row[4]}
		return userinfo

	#settingsdb.execute('SELECT * FROM userinfo WHERE username=?', username)
	#pprint(settingsdb)
	#return settingsdb.fetchone()
	#print(settingsdb.fetchone())




def createdb():
	"""
	since: 0.0.1

	This function creates a new settings db file for storing userinfo, connections etc
	"""

	settingsdb = sqlite3.connect(SETTINGSDB)
	settingsdb.execute("CREATE TABLE settingsinfo(dbVersion INTEGER, winX INTEGER, winY INTEGER, winWidth INTEGER, winHeight INTEGER, created INTEGER);")
	settingsdb.execute("INSERT INTO settingsinfo values ({0}, {1}, {2}, {3}, {4}, strftime('now'));".format(DBVERSION, 64, 64, 600, 400))

	settingsdb.execute("CREATE TABLE userinfo(username STRING, password STRING, host STRING, port INTEGER, created INTEGER);")


	settingsdb.commit()
	settingsdb.close()

