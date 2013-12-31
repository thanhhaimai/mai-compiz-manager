import xml.etree.ElementTree as ET
from collections import namedtuple

class Key(namedtuple('Key', ['schema_id', 'name', 'value_type', 'default',
                             'summary', 'description'])):
    def __new__(cls, schema_id, name, value_type, default, summary='empty',
                description='empty'):
        return super(Key, cls).__new__(cls, schema_id, name, value_type, default,
                                       summary, description)

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

if __name__ == "__main__":
    for schema in get_all_schema_roots():
        keys = parse_schema(schema)
        for key in keys:
            print key

