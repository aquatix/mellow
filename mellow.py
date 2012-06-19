#!/usr/bin/python
from gi.repository import Gtk
from pprint import pprint
#import sqlite3

#from "../py-sonic/py-sonic/"
#from importlib import import_module
#importlib.import_module("../py-sonic/py-sonic/")
#import_module('../py-sonic/py-sonic/', 'pysonic')

import libsonic

import settings

userinfo = ''


class MyWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Hello World")

		self.button = Gtk.Button(label="Connect")
		self.button.connect("clicked", self.on_button_clicked)
		self.add(self.button)

	def on_button_clicked(self, widget):
		print("Hello World")

		#settings.createdb()
		userinfo = settings.login()
		pprint(userinfo)

		conn = libsonic.Connection(userinfo['host'], userinfo['username'], userinfo['password'], userinfo['port'])

		songs = conn.getRandomSongs(size=2)
		pprint(songs)

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
