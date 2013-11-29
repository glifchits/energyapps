
import sys
import os
import xml.etree.ElementTree as ET

from sqlalchemy.engine import create_engine
engine = create_engine('postgresql://localhost', echo=True)
connection = engine.connect()

try:
    filename = sys.argv[1]
    assert(os.path.isfile(filename))
except ValueError, AssertionError:
    sys.stderr.write('Usage: %s [filename]\n' % sys.argv[0])
    sys.exit()

tree = ET.parse(filename)
root = tree.getroot()

ENTRY = '{http://www.w3.org/2005/Atom}entry'
CONTENT = '{http://www.w3.org/2005/Atom}content'

USAGE_POINT = '{http://naesb.org/espi}UsagePoint'
SERVICE_CATEGORY = '{http://naesb.org/espi}ServiceCategory'
KIND = '{http://naesb.org/espi}kind'
LOCAL_TIME = '{http://naesb.org/espi}LocalTimeParameters'
METER_READING = '{http://naesb.org/espi}MeterReading'
INTERVAL_BLOCK = '{http://naesb.org/espi}IntervalBlock'
READING_TYPE = '{http://naesb.org/espi}ReadingType'

kind = root.findall(ENTRY)[0].find(CONTENT).find(USAGE_POINT)\
        .find(SERVICE_CATEGORY).find(KIND)
dst_end, dst_offset, dst_start, tz_offset = root.findall(ENTRY)[1]\
        .find(CONTENT).find(LOCAL_TIME).getchildren()
#reading_info = root.findall(ENTRY)[2].find(CONTENT).find(METER_READING)
interval_blocks = root.findall(ENTRY)[3].find(CONTENT).findall(INTERVAL_BLOCK)
reading_type = root.findall(ENTRY)[4].find(CONTENT).find(READING_TYPE)

accumulation_behaviour, commodity, currency, data_qualifier, flow_direction, \
interval_length, kind, phase, multiplier, time_attribute, uom\
    = reading_type.getchildren()


print '-' * 80
print ''
print kind.text
print dst_end.text, dst_offset.text, dst_start.text, tz_offset.text

for block in interval_blocks:
    children = block.getchildren()
    interval = children[0]
    interval_readings = children[1:]

    duration, start = interval.getchildren()
    for i_reading in interval_readings:
        cost, time_period, value = i_reading.getchildren()
        duration, start = time_period.getchildren()

