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

		self.connectButton = Gtk.Button(label="Connect")
		self.connectButton.connect("clicked", self.on_connectbutton_clicked)
		#self.add(self.button)
		self.grid.add(self.connectButton)


		# Artists list
		self.artistliststore = Gtk.ListStore(int, str)
		self.artisttreeview = Gtk.TreeView(model=self.artistliststore)
		#self.artisttreeview.set_fixed_height_mode(True)
		self.grid.attach_next_to(self.artisttreeview, self.connectButton, Gtk.PositionType.BOTTOM, 1, 1)

		self.load_artist_list()

		# Album list
		self.albumliststore = Gtk.ListStore(int, str)
		self.albumtreeview = Gtk.TreeView(model=self.albumliststore)
		self.grid.attach_next_to(self.albumtreeview, self.connectButton, Gtk.PositionType.RIGHT, 1, 2)

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
			artists = conn.getIndexes()
		except urllib.error.HTTPError:
			print("authfail while getting artists")
			return -1
		#pprint(artists)

		mainwindow.artistliststore.clear()

		for artistLetter in artists['indexes']['index']:
			#pprint(artistLetter)
			theseArtists = artistLetter['artist']
			thisLetter = artistLetter['name']
			#print(thisLetter)

			if thisLetter == 'A':
				for thisArtist in theseArtists:
					mainwindow.artistliststore.append([thisArtist['id'], thisArtist['name']])

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
