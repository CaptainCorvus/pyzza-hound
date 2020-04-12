import socket
import datetime
import gpiozero

import common
from SensorDB import DataInterface


logger = common.get_logger(__name__)

LED = gpiozero.LED

try:
    di = DataInterface()
except Exception as e:
    logger.error("Unable to connect to database.",  exc_info=True)
    raise


"""
    LEDS ordered such that index of LED in LEDS is corresponding
    bit of temp represented on display
    bit 7, is a flag bit to indicate that temp being displayed is 
    older than 10 minutes from present
"""
LEDS = (LED(26), LED(19), LED(13), LED(6),
        LED(12), LED(16), LED(20), LED(21))

def display_temp_analog(temp):
    """

    :param temp: temperature in degrees [F]
    :return: None
    """
    logger.info("Updating LEDs")
    # round temp, convert to int
    temp = int(round(temp, 0))

    # set bits from 0 to 64, do not set 128
    for led in LEDS[:7]:
        if temp & 1:
            led.on()
        else:
            led.off()
        temp = temp >> 1

def display_validity_bit(reading_time):
    """
    Set bit 7 of the display, if the time of reading is within
    the last minute, the bit is 0, else if time > 10 minutes old,
    bit is 1 ie LED on.

    :param reading_time:
    :return: None
    """
    tnow = datetime.datetime.now()

    # create 10 minute window from now to 10m ago
    tplus_ten = tnow - datetime.timedelta(minutes=10)

    if reading_time < tplus_ten:
        # reading time older than ten minutes, set high bit
        LEDS[-1].on()
    else:
        LEDS[-1].off()


def get_latest_data():
    host = socket.gethostname()
    last_reading = di.get_last_temp_reading(host)

    temp = last_reading['tempf']
    time = last_reading['time']

    return temp, time



while True:
    logger.info("updating LEDs")

    # get the last data from the database
    temp, time = get_latest_data()

    # set bits 0-6 on display




