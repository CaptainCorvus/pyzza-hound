import DeviceInfo
import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, query
from sqlalchemy import Column, Integer, String, DateTime, Float, VARCHAR
import numpy as np


"""
Standard interface for connecting to the Sensor database
"""

engine = create_engine('mysql://trevor:doylelovespizza@pumpkin/Sensors')
Base   = declarative_base()

# create session
Session = sessionmaker(bind=engine)


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


class Testing(Base):
    __tablename__ = 'testing'
    id = Column(Integer, primary_key=True)
    comment = Column(VARCHAR(64))


Devices.__table__.create(bind=engine, checkfirst=True)
TemperatureData.__table__.create(bind=engine, checkfirst=True)
Testing.__table__.create(bind=engine, checkfirst=True)


class DataInterface:
    def __init__(self):
        self.session = Session()

    def _parse_data(self, data):
        """
        create three lists from queried data: one with timeseries,
        the other two with the temp in C/F
        :param data: a list of dicts
        :return: timeseries <datetime>, tempc <list>, tempf <list>
        """
        times = list()
        tempc = list()
        tempf = list()
        for row in data:
            curr_row = vars(row)
            times.append(curr_row['Time'].strftime('%Y-%m-%d %H:%M:%S'))
            tempc.append(curr_row['Temp_c'])
            tempf.append(curr_row['Temp_f'])

        return times, tempc, tempf

    def add_device(self, new_device):
        """
        TODO
        :param new_device:
        :return:
        """
        if not isinstance(new_device, dict):
            raise TypeError

        entry = Devices(
            Device   = new_device['device'],
            Alias    = new_device['alias'],
            Location = new_device['location']
        )
        self.session.add(entry)
        self.session.commit()

    def add_temperature_reading(self, new_reading):
        """
        Add a temperature reading to the mysqldb
        :param new_reading:
        :return:
        """
        if not isinstance(new_reading, dict):
            raise TypeError

        entry = TemperatureData(**new_reading)
        self.session.add(entry)
        self.session.commit()

    def _get_temp_stats(self, time, tempc, tempf):
        """
        Return a dict with stats for provided data

        :param time:
        :param tempc: temperature data in Celsius
        :type tempc: numpy.array
        :param tempf: temperature data in Fehrenheit
        :type tempf: numpy.array

        :return: stats of data
        """
        if tempf is None or len(tempf) == 0:
            return

        stats = dict()

        # get indices of min/max
        id_max = np.argmax(tempf)
        id_min = np.argmin(tempf)

        stats['mean']   = np.mean(tempf)
        stats['std']    = np.std(tempf)
        stats['max']    = tempf[id_max]
        stats['min']    = tempf[id_min]
        stats['tmax']   = time[id_max]
        stats['tmin']   = time[id_min]

        return stats


    def get_temp_readings(self, tstart, tstop, device=None):
        """

        :param tstart:
        :param tstop:
        :param device:
        :return:
        """
        # tstart, tstop should be datetime objects
        if not isinstance(tstart, datetime.datetime) or\
                not isinstance(tstop, datetime.datetime):
            raise TypeError
        if device is None:
            device = DeviceInfo.DEFAULT_DEVICES['temperature']

        # build the query
        qry = self.session.query(TemperatureData)\
            .filter(TemperatureData.Time >= tstart)\
            .filter(TemperatureData.Time <= tstop)\
            .filter(TemperatureData.Device == device).all()
        time, tempc, tempf = self._parse_data(qry)



        stats = self._get_temp_stats(
            np.array(time),
            np.array(tempc),
            np.array(tempf)
        )

        return device, time, tempc, tempf, stats


    def add_to_testing(self, test_entry):
        if not isinstance(test_entry, dict):
            raise TypeError

        entry = Testing(**test_entry)
        self.session.add(entry)
        self.session.commit()

