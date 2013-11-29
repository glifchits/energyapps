from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Reading(Base):
    __tablename__ 'reading'

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


class Interval(Base):
    __tablename__ 'interval'

    id = Column(Integer, primary_key=True)
    duration = Column(Integer)
    start = Column(Integer)
    reading_id = Column(Integer, ForeignKey('reading.id'))

    reading = relationship("Reading", backref=backref('readings',
        order_by=id))


class IntervalReading(Base):
    __tablename__ = 'interval_reading'

    id = Column(Integer, primary_key=True)
    interval_id = Column(Integer, ForeignKey('interval.id'))
    start = Column(Integer)
    duration = Column(Integer)
    cost = Column(Integer)
    value = Column(Integer)

    interval = relationship("Interval", backref=backref('interval',
        order_by=id))

