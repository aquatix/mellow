#!/usr/bin/python3
from gi.repository import Gtk
from gi.repository import GLib

from pprint import pprint
import urllib
#import sqlite3

import threading

#from "../py-sonic/py-sonic/"
#from importlib import import_module
#importlib.import_module("../py-sonic/py-sonic/")
#import_module('../py-sonic/py-sonic/', 'pysonic')

import libsonic

__version__ = '0.0.1'

import settings
import cache

appsettings = settings.settings()
serverinfo = ''


# Use threads                                       
GLib.threads_init()


class MainWindow(Gtk.Window):

	# == GUI Elements ======

	def __init__(self):
		Gtk.Window.__init__(self, title="Mellow")


		#self.vpan = Gtk.VPaned()
		#self.hpan = Gtk.HPaned()

		#self.vpan.show()
		#self.hpan.show()

		#self.vBox1.pack_end(self.hpan, True, True, 0)
		#self.hpan.pack1(self.vpan, False, True)


		# Start the grid
		self.grid = Gtk.Grid()
		self.add(self.grid)


		# Toolbar above the artists list
		self.toolBar = Gtk.Toolbar()
		self.grid.add(self.toolBar)
		context = self.toolBar.get_style_context()
		context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)


		#self.connectButton = Gtk.Button(label="Connect")
		#self.connectButton.connect("clicked", self.onConnectbuttonClicked)
		#self.add(self.button)
		#self.grid.add(self.connectButton)

		#self.connectButton = Gtk.ToolButton()
		self.connectButton = Gtk.ToolButton(stock_id=Gtk.STOCK_CONNECT)
		self.connectButton.set_property("visible",True)
		#self.connectButton.set_property("icon_name","list-add-symbolic")
		self.connectButton.connect("clicked", self.onConnectbuttonClicked)
		self.toolBar.add(self.connectButton)


		self.refreshButton = Gtk.ToolButton()
		self.refreshButton.set_property("visible",True)
		self.refreshButton.set_property("icon_name","view-refresh")
		self.refreshButton.set_label("Refresh artists from server")
		self.refreshButton.connect("clicked", self.onRefreshbuttonClicked)
		self.toolBar.add(self.refreshButton)


		# Playback toolbar with the widgets you might expect there
		self.playbackToolBar = Gtk.Toolbar()
		self.grid.add(self.playbackToolBar)
		context = self.playbackToolBar.get_style_context()
		context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)

		self.previousButtonButton = Gtk.ToolButton(stock_id=Gtk.STOCK_MEDIA_PREVIOUS)
		self.previousButtonButton.connect("clicked", self.onPreviousButtonbuttonClicked)
		self.playbackToolBar.add(self.previousButtonButton)

		self.playButton = Gtk.ToolButton(stock_id=Gtk.STOCK_MEDIA_PLAY)
		self.playButton.connect("clicked", self.onPlaybuttonClicked)
		self.playbackToolBar.add(self.playButton)

		self.stopButton = Gtk.ToolButton(stock_id=Gtk.STOCK_MEDIA_STOP)
		self.stopButton.connect("clicked", self.onStopbuttonClicked)
		self.playbackToolBar.add(self.stopButton)

		self.nextButton = Gtk.ToolButton(stock_id=Gtk.STOCK_MEDIA_NEXT)
		self.nextButton.connect("clicked", self.onNextbuttonClicked)
		self.playbackToolBar.add(self.nextButton)


		# Artists list
		self.artistscroll = Gtk.ScrolledWindow()
		self.artistscroll.set_hexpand(True)
		self.artistscroll.set_vexpand(True)
		#self.grid.attach(artistscroll, 0, 1, 3, 1)
		self.grid.attach_next_to(self.artistscroll, self.toolBar, Gtk.PositionType.BOTTOM, 1, 1)

		self.artistliststore = Gtk.ListStore(int, str)
		self.artisttreeview = Gtk.TreeView(model=self.artistliststore)
		select = self.artisttreeview.get_selection()
		select.connect("changed", self.onArtistViewchanged)
		self.artistscroll.add(self.artisttreeview)

		self.loadArtistList()


		# Album list
		self.albumscroll = Gtk.ScrolledWindow()
		self.albumscroll.set_hexpand(True)
		self.albumscroll.set_vexpand(True)
		#self.grid.attach_next_to(self.albumscroll, self.connectButton, Gtk.PositionType.RIGHT, 1, 2)
		self.grid.attach_next_to(self.albumscroll, self.artistscroll, Gtk.PositionType.RIGHT, 1, 2)

		self.albumliststore = Gtk.ListStore(int, str)
		self.albumtreeview = Gtk.TreeView(model=self.albumliststore)
		#self.albumtreeview.connect(
		self.albumscroll.add(self.albumtreeview)

		pprint(self.artistliststore.get(0))
		#self.loadAlbumList(self.artistliststore.get(1))


		#self.set_default_size(gtk.gdk.screen_width(),500)
		self.set_default_size(appsettings['winWidth'], appsettings['winHeight'])
		self.move(appsettings['winX'], appsettings['winY']);



	def loadArtistList(mainwindow):
		"""
		Refresh artists listing
		"""
		# fetch artists, @TODO: has ifModifiedSince for caching
		serverinfo = settings.getServerInfo()
		print(serverinfo)

		hasCache = cache.haveCachedArtists(serverinfo)

		if False == hasCache:
			mainwindow.onRefreshbuttonClicked(mainwindow)
			#artists = mainwindow.getArtistsFromServer(serverinfo)
			#cache.saveArtists(serverinfo, artists)
		else:
			print("get from cache")


		artists = cache.getArtists(serverinfo)


		mainwindow.artistliststore.clear()
		previousLetter = ''

		for artist in artists:
			#print(artist)
			thisLetter = artist['indexLetter']
			#print(thisLetter)

			if thisLetter != previousLetter:
				#print(thisLetter)
				previousLetter = thisLetter

			mainwindow.artistliststore.append([artist['id'], artist['name']])

		#renderer_text = Gtk.CellRendererText()
		#column_text = Gtk.TreeViewColumn("ID", renderer_text, text=0)
		#mainwindow.artisttreeview.append_column(column_text)

		renderer_artistName = Gtk.CellRendererText()
		#renderer_editabletext.set_property("editable", True)

		column_artistName = Gtk.TreeViewColumn("Artist", renderer_artistName, text=1)
		mainwindow.artisttreeview.append_column(column_artistName)

		# Make 'artistname' column searchable
		mainwindow.artisttreeview.set_search_column(1)

		#renderer_editabletext.connect("edited", self.text_edited)



	#def loadAlbumList(artist, albums):
	def loadAlbumList(mainwindow, artistID):
		# Allow sorting on the column
		#self.tvcolumn.set_sort_column_id(0)

		# Allow drag and drop reordering of rows
		#self.treeview.set_reorderable(True)

		serverinfo = settings.getServerInfo()
		conn = libsonic.Connection(serverinfo['host'], serverinfo['username'], serverinfo['password'], serverinfo['port'])
		#albums = conn.getMusicDirectory(artistid)
		#albums = conn.getArtist(artistID)
		albums = cache.getAlbums(serverinfo, artistID)
		pprint(albums)

		return 42


	def onArtistViewchanged(self, selection):
		model, treeiter = selection.get_selected()
		if treeiter != None:
			print("You selected", model[treeiter][0])
			self.loadAlbumList(model[treeiter][0])




	# == Buttons ======

	def onRefreshbuttonClicked(self, widget):
		refreshThread = self.UpdateFromServerThread(self)
		refreshThread.setDaemon(True)
		refreshThread.start()


	def onPreviousButtonbuttonClicked(self, widget):
		print("Skipping backward")


	def onNextbuttonClicked(self, widget):
		print("Skipping forward")


	def onPlaybuttonClicked(self, widget):
		print("Beginning playback")


	def onStopbuttonClicked(self, widget):
		print("Stop playback")



	def onConnectbuttonClicked(self, widget):
		print("Connecting...")

		#settings.createdb()
		serverinfo = settings.getServerInfo()
		#pprint(serverinfo)

		conn = libsonic.Connection(serverinfo['host'], serverinfo['username'], serverinfo['password'], serverinfo['port'])

		songs = conn.getRandomSongs(size=2)
		pprint(songs)



	# == Subsonic remote data retrieval ======

	class UpdateFromServerThread(threading.Thread):
		def __init__(self, mainwindow):
			threading.Thread.__init__(self)
			self.mainwindow = mainwindow
			pprint(mainwindow)
			pprint(self.mainwindow)


		def run(self):
			print("Refreshing...")
			serverinfo = settings.getServerInfo()
			cache.clearArtists(serverinfo)
			cache.saveArtists(serverinfo, self.getArtistsFromServer(serverinfo))
			
			# refresh artist list in window
			self.mainwindow.loadArtistList()
			
			artists = cache.getArtists(serverinfo)

			print("also storing albums:")
			cache.clearAlbums(serverinfo)
			
			result = self.cacheAllAlbumsFromServer(serverinfo, artists)

			#print("Creating album download thread")
			# Create thread to load albums from server with
			#try:
			#	threading.Thread( target = self.cacheAllAlbumsFromServer, (serverinfo, artists, ) ).start()
			#except:
			#	print "Error: unable to start thread"


		def getArtistsFromServer(self, serverinfo):
			if {} == serverinfo:
				print("Login failed!")
				return

			try:
				conn = libsonic.Connection(serverinfo['host'], serverinfo['username'], serverinfo['password'], serverinfo['port'])
			except urllib.error.HTTPError:
				print("User/pass fail")

			print ("Getting artists")
			try:
				# @TODO: use ifModifiedSince with caching
				print("Using API ", conn.apiVersion)
				if ('1.8.0' == conn.apiVersion):
					print("getArtists()")
					artists = conn.getArtists()
					artists = artists["artists"]
				else:
					print("getIndexes()")
					artists = conn.getIndexes()
					artists = artists["indexes"]
			except urllib.error.HTTPError:
				print("authfail while getting artists")
				return -1
			except KeyError, e:
				print("[getArtistsFromServer] KeyError: something was wrong with the data")
				return -1
			#pprint(artists)
			return artists


		def cacheAllAlbumsFromServer(self, serverinfo, artists):
			if {} == serverinfo:
				print("Login failed!")
				return

			try:
				conn = libsonic.Connection(serverinfo['host'], serverinfo['username'], serverinfo['password'], serverinfo['port'])
			except urllib.error.HTTPError:
				print("User/pass fail")

			for artist in artists:
				print ("Getting albums for artist ", artist['id'])
				try:
					# @TODO: use ifModifiedSince with caching
					if ('1.8.0' == conn.apiVersion):
						albums = conn.getArtist(artist['id'])
						albums = albums["artist"]
					else:
						print("API version unsupported: need 1.8.0 or newer")
				except urllib.error.HTTPError:
					print("authfail while getting albums")
					return -1
				except KeyError, e:
					print("[getAllAlbumsFromServer] KeyError: something was wrong with the data")
					return -1
				cache.saveAlbums(serverinfo, albums)
			return True


	def getAlbumsFromServer(self, serverinfo, artistID):
		if {} == serverinfo:
			print("Login failed!")
			return

		try:
			conn = libsonic.Connection(serverinfo['host'], serverinfo['username'], serverinfo['password'], serverinfo['port'])
		except urllib.error.HTTPError:
			print("User/pass fail")

		print ("Getting albums for artist ", artistID)
		#albums = conn.getArtist(artistID)
		#pprint(albums)
		#albums = albums["artist"]
		try:
			# @TODO: use ifModifiedSince with caching
			if ('1.8.0' == conn.apiVersion):
				#print("getArtist", artistID)
				albums = conn.getArtist(artistID)
				albums = albums["artist"]
			else:
				print("API version unsupported: need 1.8.0 or newer")
		except urllib.error.HTTPError:
			print("authfail while getting albums")
			return -1
		except KeyError, e:
			print("[getAlbumsFromServer] KeyError: something was wrong with the data")
			return -1
		#pprint(albums)
		return albums


# Initialise and create the main window of the program
win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
