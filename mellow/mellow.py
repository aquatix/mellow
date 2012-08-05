#!/usr/bin/python3
from gi.repository import Gtk
from pprint import pprint
import urllib
#import sqlite3

#from "../py-sonic/py-sonic/"
#from importlib import import_module
#importlib.import_module("../py-sonic/py-sonic/")
#import_module('../py-sonic/py-sonic/', 'pysonic')

import libsonic

__version__ = '0.0.1'

import settings
import cache

appsettings = settings.settings()
userinfo = ''


class MainWindow(Gtk.Window):

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

		self.toolBar = Gtk.Toolbar()
		self.grid.add(self.toolBar)

		#self.connectButton = Gtk.Button(label="Connect")
		#self.connectButton.connect("clicked", self.on_connectbutton_clicked)
		#self.add(self.button)
		#self.grid.add(self.connectButton)

		self.connectButton = Gtk.ToolButton()
		self.connectButton.set_property("visible",True)
		self.connectButton.set_property("icon_name","list-add-symbolic")
		self.connectButton.connect("clicked", self.on_connectbutton_clicked)
		self.toolBar.add(self.connectButton)


		# Artists list
		self.artistscroll = Gtk.ScrolledWindow()
		self.artistscroll.set_hexpand(True)
		self.artistscroll.set_vexpand(True)
		#self.grid.attach(artistscroll, 0, 1, 3, 1)
		self.grid.attach_next_to(self.artistscroll, self.toolBar, Gtk.PositionType.BOTTOM, 1, 1)

		self.artistliststore = Gtk.ListStore(int, str)
		self.artisttreeview = Gtk.TreeView(model=self.artistliststore)
		self.artistscroll.add(self.artisttreeview)

		self.load_artist_list()


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
		#self.load_album_list(self.artistliststore.get(1))


		#self.set_default_size(gtk.gdk.screen_width(),500)
		self.set_default_size(appsettings['winWidth'], appsettings['winHeight'])
		self.move(appsettings['winX'], appsettings['winY']);



	def load_artist_list(mainwindow):
		"""
		Refresh artists listing
		"""
		# fetch artists, @TODO: has ifModifiedSince for caching
		userinfo = settings.login()
		print(userinfo)

		hasCache = cache.haveCachedArtists(userinfo)
		print (hasCache)

		if False == hasCache:

			if {} == userinfo:
				print("Login failed!")
				return

			try:
				conn = libsonic.Connection(userinfo['host'], userinfo['username'], userinfo['password'], userinfo['port'])
				print("conn:")
				pprint(conn)
			except urllib.error.HTTPError:
				print("User/pass fail")

			print ("Getting artists")
			try:
				# @TODO: use ifModifiedSince with caching
				artists = conn.getIndexes()
			except urllib.error.HTTPError:
				print("authfail while getting artists")
				return -1
			pprint(artists)
			cache.saveArtists(userinfo, artists)


		else:
			print("get from cache")


		artists = cache.getArtists(userinfo)
		pprint(artists)
		#return

		mainwindow.artistliststore.clear()
		previousLetter = ''

		#for artistLetter in artists['indexes']['index']:
		for artist in artists:
			thisLetter = artist['indexLetter']
			print(thisLetter)

			if thisLetter != previousLetter:
				print(thisLetter)
				previousLetter = thisLetter

			#if thisLetter == 'A':
			#	for thisArtist in theseArtists:
			#		mainwindow.artistliststore.append([thisArtist['id'], thisArtist['name']])

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



	def load_album_list(artist, albums):
		# Allow sorting on the column
		#self.tvcolumn.set_sort_column_id(0)

		# Allow drag and drop reordering of rows
		#self.treeview.set_reorderable(True)

		return 42


	def on_connectbutton_clicked(self, widget):
		print("Connecting...")

		#settings.createdb()
		userinfo = settings.login()
		#pprint(userinfo)

		conn = libsonic.Connection(userinfo['host'], userinfo['username'], userinfo['password'], userinfo['port'])

		songs = conn.getRandomSongs(size=2)
		pprint(songs)

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
