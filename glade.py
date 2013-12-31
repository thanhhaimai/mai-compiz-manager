#!/usr/bin/env python

import sys
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

class HelloWorld:
    def __init__(self):
        self.gladefile = "./gui.glade"
        self.wTree = gtk.glade.XML(self.gladefile)

        self.window = self.wTree.get_widget("MainWindow")
        if self.window:
            self.window.connect("destroy", gtk.main_quit)

if __name__ == "__main__":
    window = HelloWorld()
    gtk.main()
