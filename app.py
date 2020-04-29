import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio
import window

win = window.Window()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
del win