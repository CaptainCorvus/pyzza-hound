import gpiozero
import common

logger = common.get_logger(__name__)

LED = gpiozero.LED

LEDS = (LED(26), LED(19), LED(13), LED(6),
        LED(12), LED(16), LED(20), LED(21))

def display_temp_analog(temp):
    logger.info("Updating LEDs")
    # round temp, convert to int
    temp = int(round(temp, 0))
    for led in LEDS:
        if temp & 1:
            led.on()
        else:
            led.off()
        temp = temp >> 1