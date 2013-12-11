import xml.etree.ElementTree as ET


ENTRY = '{http://www.w3.org/2005/Atom}entry'
CONTENT = '{http://www.w3.org/2005/Atom}content'
TITLE = '{http://www.w3.org/2005/Atom}title'
ID = '{http://www.w3.org/2005/Atom}id'
LINK = '{http://www.w3.org/2005/Atom}link'

USAGE_POINT = '{http://naesb.org/espi}UsagePoint'
SERVICE_CATEGORY = '{http://naesb.org/espi}ServiceCategory'
KIND = '{http://naesb.org/espi}kind'
LOCAL_TIME = '{http://naesb.org/espi}LocalTimeParameters'
METER_READING = '{http://naesb.org/espi}MeterReading'
USAGE_POINT = '{http://naesb.org/espi}UsagePoint'
INTERVAL_BLOCK = '{http://naesb.org/espi}IntervalBlock'
READING_TYPE = '{http://naesb.org/espi}ReadingType'


class Entry(object):

    NODE_TAG = None

    def __init__(self, root):
        self.root = root
        self.links = [link.attrib for link in root.findall(LINK)]

    @property
    def self_path(self):
        for link in self.links:
            rel = link['rel']
            if rel == 'self':
                return link['href']

    @property
    def related(self):
        rels = []
        for link in self.links:
            rel = link['rel']
            if rel == 'related':
                rels.push(link['href'])
        return rels

    @property
    def parent_path(self):
        for link in self.links:
            rel = link['rel']
            if rel == 'up':
                return link['href']

    @property
    def id(self):
        return self.root.find(ID)

    @property
    def title(self):
        return self.root.find(TITLE)

    @property
    def content(self):
        return self.root.find(CONTENT)

    @property
    def node(self):
        assert self.NODE_TAG is not None
        return self.content.find(self.NODE_TAG)


class UsagePoint(Entry):
    NODE_TAG = USAGE_POINT

    @property
    def kind(self):
        return self.node.find(SERVICE_CATEGORY).find(KIND)


class MeterReading(Entry):
    NODE_TAG = METER_READING


class ReadingType(Entry):
    NODE_TAG = READING_TYPE
    '''
    def __init__(self):
        self.accumulation_behaviour, \
        self.commodity, \
        self.currency, \
        self.data_qualifier, \
        self.flow_direction, \
        self.interval_length, \
        self.kind, \
        self.phase, \
        self.multiplier, \
        self.time_attribute, \
        self.uom \
            = self.node.getchildren()
    '''


class IntervalBlock(Entry):

    @property
    def interval_blocks(self):
        return self.content.findall(INTERVAL_BLOCK)

    @property
    def interval_readings(self):
        return self.content.findall(INTERVAL_READING)


class ElectricPowerUsageSummary(Entry):
    pass


class LocalTimeParameters(Entry):
    NODE_TAG = LOCAL_TIME

    '''def __init__(self):
        self.dst_end, \
        self.dst_offset, \
        self.dst_start, \
        self.tz_offset \
            = self.node.getchildren()
    '''

class GreenButtonData(object):

    def __init__(self, xml_string):
        self.root = ET.fromstring(xml_string)

    def _cast_entry(self, entry):
        content = Entry(entry).content
        if content.find(INTERVAL_BLOCK) is not None:
            return IntervalBlock(entry)
        elif content.find(LOCAL_TIME) is not None:
            return LocalTimeParameters(entry)
        elif content.find(METER_READING) is not None:
            return MeterReading(entry)
        elif content.find(USAGE_POINT) is not None:
            return UsagePoint(entry)
        elif content.find(READING_TYPE) is not None:
            return ReadingType(entry)
        else:
            raise ValueError("encountered an undefined entry: %s" % entry)

    @property
    def entries(self):
        es = self.root.findall(ENTRY)
        return map(self._cast_entry, es)


if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as f:
        ns = '{http://www.w3.org/2005/Atom}'
        xml = f.read()
        eui = GreenButtonData(xml)

        for entry in eui.entries:
            print entry.self_path



