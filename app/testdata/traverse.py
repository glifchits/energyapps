import sys
import xml.etree.ElementTree as ET


def traverse(node, level):
    print '   ' * level,
    text = node.text if node.text else ''
    name = node.tag#[node.tag.find('}')+1:]
    attrib = ''
    for key, val in node.attrib.items():
        attrib += ' %s=%s' % (key, val)
    print '<%s%s>' % (name, attrib), '%s' % text.strip()

    children = node.getchildren()
    for child in children:
        traverse(child, level+1)


def parse(xml_filename):
    tree = ET.parse(xml_filename)
    root = tree.getroot()
    traverse(root, 0)


if __name__ == '__main__':
    parse(sys.argv[1])
