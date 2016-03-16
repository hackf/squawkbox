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
#  Squawk Box main control object.
#  Aaron Mavrinac <aaron@logick.ca>


import pygame
import picamera
import os
import time
from subprocess import Popen

from .hardware import SquawkBoxHardware
from .sponsor import sponsor_images


WIDTH = 1280
HEIGHT = 720
PICAM_BINARY = '/home/aaron/picam-1.4.1-binary/picam'


class SquawkBoxController(object):
    def __init__(self):
        self.hardware = SquawkBoxHardware(callback=self.record)
        self.sponsor_images = sponsor_images('/home/pi/images', WIDTH, HEIGHT)

        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT),
                                              pygame.FULLSCREEN, 32)

    def record(self, *args):
        pid = Popen([PICAM_BINARY,
                     '--alsadev', 'hw:1,0',
                     '--preview',
                     '--volume', '2'])

        time.sleep(2)
        with open('hooks/start_record', 'a'):
            os.utime('hooks/start_record', None)

        # TODO: countdown
        time.sleep(10)

        with open('hooks/stop_record', 'a'):
            os.utime('hooks/stop_record', None)
        time.sleep(2)
        pid.kill()

        (_, _, ts_files) = os.walk('rec').next()
        ts_path = os.path.join('rec', ts_files[-1])
        Popen(['ffmpeg',
               '-i',
               '-acodec', 'copy',
               '-vcodec', 'copy',
               "{}{}".format(ts_path.split('.')[0], '.mpg')])


    def mainloop(self):
        while True:
            # load a sponsor image
            image = self.sponsor_images.next()
            try:
                image = pygame.image.frombuffer(image.tobytes(),
                                                image.size, 'RGB')
                print('loaded image')
            except ValueError:
                print('bad image')
                continue

            # blank screen
            self.window.fill((0, 0, 0))

            # blit image to center of screen
            x = (WIDTH / 2) - (image.get_width() / 2)
            y = (HEIGHT / 2) - (image.get_height() / 2)
            self.window.blit(image, (x, y))
            
            # display for 10 seconds
            pygame.display.flip()
            pygame.time.wait(10000)
