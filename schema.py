from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine('postgresql://localhost', echo=True)
connection = engine.connect()

Base = declarative_base()


class Reading(Base):
    __tablename__ 'reading_type'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    # from ReadingType
    accumulation_behaviour = Column(Integer)
    commodity = Column(Integer)
    currency = Column(Integer)
    data_qualifier = Column(Integer)
    flow_direction = Column(Integer)
    interval_length = Column(Integer)
    kind = Column(Integer)
    multiplier = Column(Integer)
    uom = Column(Integer)
    # from IntervalBlock
    duration = Column(Integer)
    start = Column(Integer)
    # from ServiceCategory
    service_kind = Column(Integer)

    readings = relationship("MeterReading", order_by='MeterReading.time_start',
            backref='reading')


class MeterReading(Base):
    __tablename__ = 'meter_reading'

    id = Column(Integer, primary_key=True)
    reading_id = Column(Integer, ForeignKey('reading_type.id'))
    time_start = Column(Integer)
    time_duration = Column(Integer)
    cost = Column(Integer)

    reading = relationship("Reading", backref=backref('meter readings',
        order_by=time_start))

