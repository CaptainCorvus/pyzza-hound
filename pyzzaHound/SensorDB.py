from DeviceInfo import DEVICES
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Float, VARCHAR


"""
Standard interface for connecting to the Sensor database
"""

engine = create_engine('mysql://trevor:doylelovespizza@pumpkin/Sensors')
Base   = declarative_base()


class Devices(Base):
    __tablename__ = 'devices'
    DeviceId      = Column(Integer, primary_key=True)
    Device        = Column(VARCHAR(32))
    Alias         = Column(VARCHAR(32))
    Location      = Column(VARCHAR(32))


class TemperatureData(Base):
    __tablename__ = 'temperature_data'
    id      = Column(Integer, primary_key=True)
    Time    = Column(DateTime)
    Temp_c  = Column(Float)
    Temp_f  = Column(Float)
    Device  = Column(VARCHAR(32))


Devices.__table__.create(bind=engine, checkfirst=True)
TemperatureData.__table__.create(bind=engine, checkfirst=True)

# create session
Session = sessionmaker(bind=engine)


def add_device(new_device):
    if not isinstance(new_device, dict):
        raise TypeError
    session = Session()
    # if new_device in DEVICES.keys():
    #     return 'not a new device'

    session = Session()
    entry = Devices(
        Device   = new_device['device'],
        Alias    = new_device['alias'],
        Location = new_device['location']
    )
    session.add(entry)
    session.commit()


def add_temperature_reading(new_reading):
    if not isinstance(new_reading, dict):
        raise TypeError
    session = Session()
    entry = TemperatureData(**new_reading)
    session.add(entry)
    session.commit()

