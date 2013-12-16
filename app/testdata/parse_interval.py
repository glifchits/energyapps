import xml.etree.ElementTree as ET
import datetime

root = ET.parse("interval_fragment.xml").getroot()

for c in root.iter():
    if c.tag == '{http://naesb.org/espi}IntervalReading':
        cost, timeperiod, value = c.getchildren()
        duration, start = timeperiod.getchildren()
        dtime = datetime.datetime.fromtimestamp(int(start.text))
        print dtime

