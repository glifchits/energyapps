import xml.etree.ElementTree as ET
import warnings


ENTRY = '{http://www.w3.org/2005/Atom}entry'
CONTENT = '{http://www.w3.org/2005/Atom}content'
TITLE = '{http://www.w3.org/2005/Atom}title'
ID = '{http://www.w3.org/2005/Atom}id'
LINK = '{http://www.w3.org/2005/Atom}link'

ns2 = '{http://naesb.org/espi}'

USAGE_POINT = '%sUsagePoint' % ns2
SERVICE_CATEGORY = '%sServiceCategory' % ns2
KIND = '%skind' % ns2
LOCAL_TIME = '%sLocalTimeParameters' % ns2
METER_READING = '%sMeterReading' % ns2
INTERVAL_BLOCK = '%sIntervalBlock' % ns2
READING_TYPE = '%sReadingType' % ns2
INTERVAL_READING = '%sIntervalReading' % ns2
COST = '%scost' % ns2
START = '%sstart' % ns2
DURATION = '%sduration' % ns2
VALUE = '%svalue' % ns2
TIME_PERIOD = '%stimePeriod' % ns2


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
                rels.append(link['href'])
        return rels

    @property
    def parent_path(self):
        for link in self.links:
            rel = link['rel']
            if rel == 'up':
                return link['href']

    @property
    def id(self):
        return self.root.find(ID).text

    @property
    def title(self):
        return self.root.find(TITLE).text

    @property
    def content(self):
        return self.root.find(CONTENT)

    @property
    def node(self):
        assert self.NODE_TAG is not None
        return self.content.find(self.NODE_TAG)


class UsagePoint(Entry):
    NODE_TAG = USAGE_POINT

    meter_readings = []
    local_time = None

    @property
    def service_kind(self):
        return self.node.find(SERVICE_CATEGORY).find(KIND).text

    def add_meter_reading(self, reading):
        self.meter_readings.append(reading)


class MeterReading(Entry):
    NODE_TAG = METER_READING

    interval_block = None
    reading_type = None

    def add_interval_block(self, interval_block):
        self.interval_block = interval_block

    def add_reading_type(self, reading_type):
        self.reading_type = reading_type


def uncamel_case(string):
    s = ''
    for ch in string:
        if 65 <= ord(ch) <= 90:
            s += '_' + ch.lower()
        else:
            s += ch
    return s


class ReadingType(Entry):
    NODE_TAG = READING_TYPE

    def __getattr__(self, key):
        key = uncamel_case(key)
        children = self.node.getchildren()
        for child in children:
            if child.tag.endswith(key):
                return child.text
        return None


class Interval(object):

    def __init__(self, node):
        self.node = node

    @property
    def start(self):
        return self.node.find(TIME_PERIOD).find(START).text

    @property
    def duration(self):
        return self.node.find(TIME_PERIOD).find(DURATION).text

    @property
    def cost(self):
        cost_node = self.node.find(COST)
        if cost_node is not None: return cost_node.text

    @property
    def value(self):
        value_node = self.node.find(VALUE)
        if value_node is not None: return value_node.text


class IntervalBlock(Entry):

    @property
    def interval_blocks(self):
        return self.content.findall(INTERVAL_BLOCK)

    @property
    def interval_readings(self):
        readings = []
        for block in self.interval_blocks:
            for reading in block.findall(INTERVAL_READING):
                readings.append(Interval(reading))
        return readings


class ElectricPowerUsageSummary(Entry):
    pass


class LocalTimeParameters(Entry):
    NODE_TAG = LOCAL_TIME

    @property
    def dst_end_rule(self):
        return self.node.getchildren()[0].text

    @property
    def dst_offset(self):
        return self.node.getchildren()[1].text

    @property
    def dst_start_rule(self):
        return self.node.getchildren()[2].text

    @property
    def tz_offset(self):
        return self.node.getchildren()[3].text


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

    def related(self, entry):
        rels = entry.related
        rel_entries = []
        for rel_link in rels:
            for entry in self.entries:
                if entry.self_path == rel_link or \
                    entry.parent_path == rel_link:
                    rel_entries.append(entry)
                    break
        assert len(rel_entries) == len(rels)
        return rel_entries

    def form_tree(self):
        usage_point = [e for e in self.entries if e.NODE_TAG == USAGE_POINT]
        assert len(usage_point) == 1
        usage_point = usage_point[0]

        local_time = [e for e in self.entries if e.NODE_TAG == LOCAL_TIME]
        if len(local_time) == 1:
            usage_point.local_time = local_time[0]
        else:
            usage_point.local_time = None

        meter_readings = [e for e in self.entries
                if e.NODE_TAG == METER_READING]

        for reading in meter_readings:
            interval_block, reading_type = self.related(reading)
            if interval_block.NODE_TAG == READING_TYPE:
                interval_block, reading_type = reading_type, interval_block
            reading.add_interval_block(interval_block)
            reading.add_reading_type(reading_type)
            usage_point.add_meter_reading(reading)

        return usage_point


def traverse_eui(eui, level, entry):
    pad = '  ' * level
    print "%s %s" % (pad, entry)
    related = eui.related(entry)
    for relative in related:
        traverse_eui(eui, level+1, relative)


if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as f:
        ns = '{http://www.w3.org/2005/Atom}'
        xml = f.read()
        eui = GreenButtonData(xml)

        for entry in eui.entries:
            print 'entry:', entry
        print ''

        usage_point = eui.form_tree()
        print 'usage point:', usage_point
        print ' local time:', usage_point.local_time
        for reading in usage_point.meter_readings:
            print '   meter reading:', reading
            print '     reading type:', reading.reading_type
            print '     interval block:', reading.interval_block



