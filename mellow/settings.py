import sqlite3
import os
from pprint import pprint

#import configparser	# python 3
import ConfigParser	# python 2.x


#print(sqlite3.version_info)
#print(sqlite3.sqlite_version_info)
#print(sqlite3.__file__)

DBVERSION = 1
DBDIR = os.path.join(os.environ['HOME'], '.config/mellow')
DBFILE = 'mellow.sqlite'
CONFFILE = 'config.ini'
SETTINGSDB = os.path.join(DBDIR, DBFILE)
CONFIGFILE = os.path.join(DBDIR, CONFFILE)


def settings():
	"""
	Fetches the app settings, create the settings dir and file if not existing yet

	[~/.config/mellow/mellow.db]
	~/.config/mellow/config.ini
	"""

	# Check whether the settings db exists
	#if not os.path.isdir(DBDIR):
	#	os.makedirs(DBDIR)
	#if not os.path.isfile(SETTINGSDB):
	#	createdb()

	#settingsdb = sqlite3.connect(SETTINGSDB)
	#for row in settingsdb.execute('SELECT dbVersion, winX, winY, winWidth, winHeight, created FROM settingsinfo'):
	#	print(row)
	#	settingsinfo = {'dbVersion': row[0], 'winX': row[1], 'winY': row[2], 'winWidth': row[3], 'winHeight': row[4], 'created': row[5]}
	#	return settingsinfo


	#config = configparser.ConfigParser()
	#config = ConfigParser.SafeConfigParser({'winX': 64, 'winY': 64, 'winWidth': 600, 'winHeight': 400})
	config = ConfigParser.SafeConfigParser({'winX': 64, 'winY': 64, 'winWidth': 600, 'winHeight': 400})

	pprint(CONFIGFILE)

	# Check whether the settings db exists
	if not os.path.isdir(DBDIR):
		os.makedirs(DBDIR)
	if not os.path.isfile(CONFIGFILE):
		#config['WINDOW'] = {'winX': 64, 'winY': 64, 'winWidth': 600, 'winHeight': 400}
		#config['WINDOW'] = {'winX': 64, 'winY': 64, 'winWidth': 600, 'winHeight': 400}
		#config['WINDOW']['winX'] = 64
		#config['WINDOW']['winY'] = 64
		#config['WINDOW']['winWidth'] = 600
		#config['WINDOW']['winHeight'] = 400

		print('whoa')

		newconfig = ConfigParser.RawConfigParser()
		newconfig.add_section('WINDOW')
		newconfig.set('WINDOW', 'winX', '64')
		newconfig.set('WINDOW', 'winY', '64')
		newconfig.set('WINDOW', 'winWidth', '600')
		newconfig.set('WINDOW', 'winHeight', '400')

		pprint(newconfig)

		with open(CONFIGFILE, 'wb') as configfile:
			newconfig.write(configfile)

	config.read(CONFIGFILE)
	#settingsinfo = {'winX': config['WINDOW']['winX'], 'winY': config['WINDOW']['winY'], 'winWidth': config['WINDOW']['winWidth'], 'winHeight': config['WINDOW']['winHeight']}
	try:
		settingsinfo = {'winX': int(config.get('WINDOW','winX')), 'winY': int(config.get('WINDOW', 'winY')), 'winWidth': int(config.get('WINDOW','winWidth')), 'winHeight': int(config.get('WINDOW','winHeight'))}
	except ConfigParser.NoOptionError:
		print ('Could not find a setting')
	pprint(settingsinfo)
	return settingsinfo


#print(config['DEFAULT']['path'])     # -> "/path/name/"
#config['DEFAULT']['path'] = '/var/shared/'    # update
#config['DEFAULT']['default_message'] = 'Hey! help me!!'   # create

#with open('FILE.INI', 'w') as configfile:    # save
#    config.write(configfile)




def getServerInfo():
	"""
	since: 0.0.1

	This function logs the application into the remote Subsonic server
	"""

	settingsdb = sqlite3.connect(SETTINGSDB)

	# for the time, default to 'michiel'
	username = ('admin',)
	userinfo = {}

	for row in settingsdb.execute('SELECT username, password, host, port, created FROM userinfo WHERE username=?', username):
		print(row)
		userinfo = {'username': row[0], 'password': row[1], 'host': row[2], 'port': row[3], 'created': row[4]}
		#print('userinfo:')
		#print(userinfo)

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

