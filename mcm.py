#!/usr/bin/python3

# TODO(thanhhaimai): use Glade MCV

from gi.repository import Gtk, Gio, GLib
import xml.etree.ElementTree as ET
from collections import namedtuple

def get_current_profile():
    setting = Gio.Settings.new("org.compiz")
    return setting.get_string("current-profile")

PROFILE = get_current_profile()

class Key:
    def __init__(self,  schema_id, name, value_type, default, summary, description, value=None):
        self.schema_id = schema_id
        self.name = name
        self.value_type = value_type
        self.default = default
        self.summary = summary
        self.description = description
        self.value = value
        self.plugin_name = self.schema_id.split('.')[-1]
        self.path = "/org/compiz/profiles/%s/plugins/%s/" % (PROFILE, self.plugin_name)

    def _get_setting(self):
        setting = Gio.Settings.new_with_path(self.schema_id, self.path)
        return setting

    def set_value(self, value):
        print("Writing value for %s:%s %s %s" % (self.schema_id, self.path, self.name, value))
        setting = self._get_setting()
        gvariant = setting.get_value(self.name)
        new_value = GLib.Variant.parse(gvariant.get_type(), value, None, None)
        self._get_setting().set_value(self.name, new_value)
        self.value = None
        print("Wrote value: %s" % self.get_value())

    def get_value(self):
        if not self.value:
            setting = self._get_setting()
            if setting:
                gvariant = setting.get_value(self.name)
                self.value = gvariant.print_(self.value_type)
            else:
                return "<ERROR>"

        return self.value

def get_all_schema_roots():
    roots = []
    with open("./compiz_schemas") as infile:
        for line in infile:
            if not line.startswith("#"):
                roots.append(ET.parse(line.strip()).getroot())

    return roots

def parse_schema(root):
    ret = []
    schemas = root.findall('schema')
    for schema in schemas:
        schema_id = schema.attrib['id']
        if schema_id == "org.compiz":
            continue

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
        self.maximize()

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

        value = key.get_value()

        schema_label = Gtk.Label(key.schema_id)
        box.pack_start(schema_label, False, False, 0)

        name_label = Gtk.Label(key.name)
        box.pack_start(name_label, False, False, 0)

        value_entry = Gtk.Entry()
        value_entry.set_text(value)
        value_entry.connect("activate", lambda entry:
                            key.set_value(entry.get_text()))
        box.pack_start(value_entry, False, False, 0)

        default_label = Gtk.Label(key.default)
        default_label.set_selectable(True)
        box.pack_start(default_label, False, False, 0)

        return box

if __name__ == "__main__":
    print("Loading profile: %s" % PROFILE)
    win = McmWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
