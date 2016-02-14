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
#  GPIO interface for Squawk Box record button.
#  Aaron Mavrinac <aaron@logick.ca>


import RPIO


class SquawkBoxHardware(object):
    "Squawk Box hardware interface."
    button_pin = 17

    def __init__(self, callback):
        RPIO.setmode(RPIO.BCM)
        RPIO.setup(self.button_pin, RPIO.IN, pull_up_down=RPIO.PUD_DOWN)
        RPIO.add_interrupt_callback(self.button_pin, callback, edge='rising',
                                    debounce_timeout_ms=1000)

    def __enter__(self):
        RPIO.wait_for_interrupts(threaded=True)

    def __exit__(self, rtype, value, traceback):
        RPIO.cleanup()
