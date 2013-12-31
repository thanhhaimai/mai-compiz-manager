#!/usr/bin/python3
from gi.repository import Gtk
import xml.etree.ElementTree as ET
from collections import namedtuple

Key = namedtuple('Key', ['schema_id', 'name', 'value_type', 'default', 'summary', 'description'])

def get_all_schema_roots():
    roots = []
    with open("./compiz_schemas") as infile:
        for line in infile:
            roots.append(ET.parse(line.strip()).getroot())

    return roots

def parse_schema(root):
    ret = []
    schemas = root.findall('schema')
    for schema in schemas:
        schema_id = schema.attrib['id']
        keys = schema.findall('key')
        for key in keys:
            value_type = key.attrib['type']
            name = key.attrib['name']
            default = parse_child_text(key, 'default', '')
            summary = parse_child_text(key, 'summary', 'empty')
            description = parse_child_text(key, 'description', 'empty')

            ret.append(Key(schema_id, name, value_type, default, summary,
                           description))

    return ret

def parse_child_text(node, name, default):
    children = node.findall(name)
    if len(children) == 1:
        return children[0].text

    return default

class McmWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Mai Compiz Manager")

        frame = Gtk.ScrolledWindow()
        self.add(frame)

        self.box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.box.set_border_width(10)
        frame.add(self.box)

        self.loadSettings()

    def loadSettings(self):
        for schema in get_all_schema_roots():
            keys = parse_schema(schema)
            for key in keys:
                self.box.pack_start(self.makeKeyRow(key), False, False, 0)

    def makeKeyRow(self, key):
        box = Gtk.Box(spacing=6)

        schema_label = Gtk.Label(key.schema_id)
        # schema_label.set_selectable(True)

        name_label = Gtk.Label(key.name)
        # name_label.set_selectable(True)

        value_entry = Gtk.Entry()
        value_entry.set_text(key.default)

        assert(schema_label != None)
        assert(name_label != None)
        assert(value_entry != None)

        box.pack_start(schema_label, False, False, 0)
        box.pack_start(name_label, False, False, 0)
        box.pack_start(value_entry, False, False, 0)

        return box

if __name__ == "__main__":
    win = McmWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
