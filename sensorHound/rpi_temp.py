import os
import sys
import time as t
import glob
import datetime as dt


# command line switch to use local test data instead of sensor
if "-test" in sys.argv:
    base_dir      = './test_data'
    device_folder = glob.glob(base_dir + '/temp*')[0]
    device_file   = device_folder + '/test_w1_slave.txt'
else:
    # set pins
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    # set base directory
    base_dir      = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file   = device_folder + '/w1_slave'


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

    # print('valid: {0}'.format(is_valid))
    # print('temp: {0}'.format(reading))

    return is_valid, reading, dt.datetime.now()


while True:
    is_valid, temp_c, time = parse_temperature()

    # only operate on valid temperature readings
    if not is_valid:
        print("Not a valid reading")
        t.sleep(0.2)
        continue

    temp_f = _convert_c_to_f(temp_c)
    if "-p" in sys.argv:
        print("\ntime: {0}".format(time))
        print('{0} C'.format(temp_c))
        print('{0} F'.format(temp_f))

    t.sleep(1)

