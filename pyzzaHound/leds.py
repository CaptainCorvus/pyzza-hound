import socket
import datetime
import time
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

def all_off():
    """
    Set all the LEDs to off
    """
    for led in LEDS:
        if led.is_lit:
            led.off()

def check_night():
    """
    Checks if current time is between 10P and 6A.

    :return: True if between 10P and 6A, False otherwise
    :rtype: bool
    """
    
    tnow    = datetime.datetime.now()
    bedtime = datetime.time(hour=22)
    wakeup  = datetime.time(hour=6) 
    t = tnow.hour
    between_ten_and_midnight = t >= bedtime.hour and t <= 23
    between_midnight_and_six = t >= 0 and t < wakeup.hour
    
    if between_ten_and_midnight or between_midnight_and_six:
        return True
    return False


def display_temp_analog(temp):
    """
    Update bits 0 through 6 on analog display to represent
    current temperature in degrees F.

    :param temp: temperature in degrees [F]
    :return: None
    """
    logger.info("Updating LEDs")

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
    """
    return the latest temperature, rounded to an integer, and
    its corresponding timestamp

    :return: (temp <int>, time <datetime.datetime>)
    """
    host = socket.gethostname()
    last_reading = di.get_last_temp_reading(host)

    temp = last_reading['tempf']
    time = last_reading['time']

    return int(round(temp, 0)), time


def update_dance():
    """

    :return:
    """

    # turn off all leds to start the dance
    all_off()
    
    for i in range(0,2):
        for led in LEDS:
            led.on()
            time.sleep(0.1)

        for led in LEDS:
            led.off()
            time.sleep(0.1)

    # turn them off again
    all_off()



prev_temp = None
while True:
    # first check if it's night
    try:
        night = check_night()
        if night:
            logger.info("Night mode, sleeping for an hour")
            prev_temp = None
            all_off()
            time.sleep(3600)
            continue
    
        # get the last data from the database
        _temp, _time = get_latest_data()
        
        if prev_temp and prev_temp != _temp:
            logger.info("updating LEDs")
            update_dance()
        else:
            logger.info("_temp == prev_temp, no update_dance")

        logger.info("setting bits for data, time: {}, temp: {}".format(_time, _temp))

        # set bits 0-6 on display
        display_temp_analog(_temp)

        # set validity bit
        display_validity_bit(_time)
    
        # update the previous temp
        prev_temp = _temp

        # with bits set, sleep until next reading
        logger.info("Sleeping for 600")
        time.sleep(598.2)
    except Exception as e:
        logger.error("Error occured updating LEDs", exc_info=True)
        raise e
