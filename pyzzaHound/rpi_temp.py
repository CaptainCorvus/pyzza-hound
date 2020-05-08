import os
import socket
import time as t
import glob
import datetime as dt
import sys
import gpiozero

from SensorDB import DataInterface
import common

logger = common.get_logger(__name__)


# get the device name
DEVICE = socket.gethostname()

# create database interface
di = DataInterface()

# command line switch to use local test data instead of sensor
if "-test" in sys.argv:
    base_dir      = './test'
    device_folder = glob.glob(base_dir + '/temp*')[0]
    device_file   = device_folder + '/test_w1_slave.txt'
else:
    try:
        # set pins
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        logger.info('pins set up')

        # set base directory
        base_dir      = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file   = device_folder + '/w1_slave'
        logger.info('directory set, reading temp from file: {}'.format(device_file))

    except Exception as e:
        logger.error("unable to setup access to temperature device", exc_info=True)
        raise e

def _convert_c_to_f(temp_c):
    temp_f = temp_c * (9.0 / 5) + 32.
    return temp_f


def _validity_to_bool(is_valid):
    if is_valid == 'YES':
        return True
    else:
        return False


def _read_raw_temperature():
    """
    Open the '/w1_slave' file and read its contents

    :return: the contents of the file
    :rtype: list
    """
    with open(device_file, 'r') as f:
        content = f.readlines()
    return content


def parse_temperature():
    """
    The first line of the /w1_slave file tells if the reading is valid with a
    value of 'YES' or 'NO'.

    The second line of the file contains the temperature reading in degrees
    celsius.
    :return: The parsed and formatted temperature in degrees celsius
    """
    content = _read_raw_temperature()

    # get last three characters of first line
    is_valid = content[0][-4:].strip()

    # convert to boolean
    is_valid = _validity_to_bool(is_valid)

    reading  = content[1]
    reading  = float(reading.split('=')[-1].strip()) / 1e3

    return is_valid, reading, dt.datetime.now()
    

while True:
    try:
        is_valid, temp_c, time = parse_temperature()
        
        # only operate on valid temperature readings
        if not is_valid:
            logger.warning("Not a valid reading: {}".format(temp_c))
            t.sleep(0.2)
            continue

        temp_f = _convert_c_to_f(temp_c)

        # create dict from temperature reading
        reading = {
            'Time': time,
            'Temp_c': temp_c,
            'Temp_f': temp_f,
            'Device': DEVICE
        }

        # write valid readings to the database
        di.add_temperature_reading(reading)
        logger.info("valid data written to database")

        if "-p" in sys.argv:
            print("\ntime: {0}".format(time))
            print('{0} C'.format(temp_c))
            print('{0} F'.format(temp_f))

        break

    except:
        logger.error("Temperature reading failed!", exc_info=True)
        break
