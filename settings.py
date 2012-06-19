import sqlite3
from pprint import pprint

print(sqlite3.version_info)
print(sqlite3.sqlite_version_info)
print(sqlite3.__file__)

DBVERSION = 1
DBFILE = 'mellow.db'

def login():
	settingsdb = sqlite3.connect(DBFILE)

	# for the time, default to 'michiel'
	username = ('michiel',)

	for row in settingsdb.execute('SELECT username, password, host, port, created FROM userinfo WHERE username=?', username):
		print(row)
		userinfo = {'username': row[0], 'password': row[1], 'host': row[2], 'port': row[3], 'created': row[4]}
		return userinfo

	#settingsdb.execute('SELECT * FROM userinfo WHERE username=?', username)
	#pprint(settingsdb)
	#return settingsdb.fetchone()
	#print(settingsdb.fetchone())




def createdb():
	"""
	This function creates a new settings db file for storing userinfo, connections etc
	"""

	settingsdb = sqlite3.connect(DBFILE)
	settingsdb.execute("CREATE TABLE settingsinfo(dbVersion INTEGER, created INTEGER);")
	settingsdb.execute("INSERT INTO settingsinfo values ({0}, strftime('now'));".format(DBVERSION))

	settingsdb.execute("CREATE TABLE userinfo(username STRING, password STRING, host STRING, port INTEGER, created INTEGER);")
