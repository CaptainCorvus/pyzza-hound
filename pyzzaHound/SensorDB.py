from DeviceInfo import DEVICES
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String


"""
Standard interface for connecting to the Sensor database
"""

engine = create_engine('mysql://trevor:doylelovespizza@pumpkin/Sensors')
Base   = declarative_base()


class Devices(Base):
    __tablename__ = 'devices'
    DeviceId      = Column(Integer, primary_key=True)
    Device        = Column(String)
    Alias         = Column(String)
    Location      = Column(String)

class TemperatureData(Base):
    __tablename__ = 'temperature data'