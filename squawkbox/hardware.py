#
#  ####                                                ####
#  ####                                                ####        
#  ####                                                ####      ##
#  ####                                                ####    ####
#  ####  ############  ############  ####  ##########  ####  ####
#  ####  ####    ####  ####    ####  ####  ####        ########
#  ####  ####    ####  ####    ####  ####  ####        ########
#  ####  ####    ####  ####    ####  ####  ####        ####  ####
#  ####  ####    ####  ####    ####  ####  ####        ####    ####
#  ####  ############  ############  ####  ##########  ####      ####
#                              ####                                ####
#  ################################                                  ####
#             __      __              __              __      __       ####
#    |  |    |  |    [__)    |_/     (__     |__|    |  |    [__)        ####
#    |/\|    |__|    |  \    |  \    .__)    |  |    |__|    |             ##
# 
#  GPIO interface for Squawk Box hardware.
#  Aaron Mavrinac <aaron@logick.ca>


import RPIO
from max7219 import led
from max7219.font import proportional, CP437_FONT


class SquawkBoxHardware(object):
    "Squawk Box hardware interface."
    button_pin = 17

    def __init__(self, callback=None):
        RPIO.setmode(RPIO.BCM)
        RPIO.setup(self.button_pin, RPIO.IN, pull_up_down=RPIO.PUD_DOWN)
        self.matrix = led.matrix()
        if callback is not None:
            set_button_callback(callback)
        RPIO.wait_for_interrupts(threaded=True)

    def set_button_callback(self, callback):
        RPIO.add_interrupt_callback(self.button_pin, callback, edge='rising',
                                    debounce_timeout_ms=1000)

    def show_message(self, message):
        self.matrix.show_message(message, font=proportional(CP437_FONT))
