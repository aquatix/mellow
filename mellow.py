#!/usr/bin/python
from gi.repository import Gtk
from pprint import pprint
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

		# Start the grid
		self.box = Gtk.Box(spacing=6)
		self.add(self.box)

		self.connectButton = Gtk.Button(label="Connect")
		self.connectButton.connect("clicked", self.on_connectbutton_clicked)
		#self.add(self.button)
		self.box.pack_start(self.connectButton, True, True, 0)


		# Artists list
		self.liststore = Gtk.ListStore(str, str)
		self.liststore.append(["Fedora", "http://fedoraproject.org/"])
		self.liststore.append(["Slackware", "http://www.slackware.com/"])
		self.liststore.append(["Sidux", "http://sidux.com/"])

		treeview = Gtk.TreeView(model=self.liststore)

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Text", renderer_text, text=0)
		treeview.append_column(column_text)

		renderer_editabletext = Gtk.CellRendererText()
		renderer_editabletext.set_property("editable", True)

		column_editabletext = Gtk.TreeViewColumn("Editable Text", renderer_editabletext, text=1)
		treeview.append_column(column_editabletext)

		#renderer_editabletext.connect("edited", self.text_edited)

		self.box.pack_start(treeview, True, True, 0)
		#self.add(treeview)


		self.load_artist_list()


		#self.set_default_size(gtk.gdk.screen_width(),500)
		self.set_default_size(appsettings['winWidth'], appsettings['winHeight'])
		self.move(appsettings['winX'], appsettings['winY']);



	def load_artist_list(mainwindow):
		"""
		Refresh artists listing
		"""

		mainwindow.artistliststore = Gtk.ListStore(int, str)

		# fetch artists, @TODO: has ifModifiedSince for caching
		userinfo = settings.login()
		conn = libsonic.Connection(userinfo['host'], userinfo['username'], userinfo['password'], userinfo['port'])

		artists = conn.getIndexes()
		#pprint(artists)

		for artistLetter in artists['indexes']['index']:
			pprint(artistLetter)
			theseArtists = artistLetter['artist']
			thisLetter = artistLetter['name']
			print(thisLetter)

			if thisLetter == 'A':
				for thisArtist in theseArtists:
					mainwindow.artistliststore.append([thisArtist['id'], thisArtist['name']])


		artisttreeview = Gtk.TreeView(model=mainwindow.artistliststore)

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("ID", renderer_text, text=0)
		artisttreeview.append_column(column_text)

		renderer_artistName = Gtk.CellRendererText()
		#renderer_editabletext.set_property("editable", True)

		column_artistName = Gtk.TreeViewColumn("Artist", renderer_artistName, text=1)
		artisttreeview.append_column(column_artistName)

		# Make 'artistname' column searchable
		artisttreeview.set_search_column(1)

		#renderer_editabletext.connect("edited", self.text_edited)

		mainwindow.box.pack_start(artisttreeview, True, True, 0)



	def on_connectbutton_clicked(self, widget):
		print("Connecting...")

		#settings.createdb()
		userinfo = settings.login()
		pprint(userinfo)

		conn = libsonic.Connection(userinfo['host'], userinfo['username'], userinfo['password'], userinfo['port'])

		songs = conn.getRandomSongs(size=2)
		pprint(songs)

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
