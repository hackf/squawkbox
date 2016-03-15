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
#  Squawk Box sponsor image generator.
#  Aaron Mavrinac <aaron@logick.ca>


import glob
import os.path
import math
from PIL import Image


def sponsor_images(image_dir, max_width, max_height):
    while True:
        for fname in glob.glob(os.path.join(image_dir, '*.jpg')):
            image = Image.open(fname, 'r')
            width, height = image.size
            if width < max_width and height < max_height:
                yield image
            else:
                scale = min(float(max_width) / float(width),
                            float(max_height) / float(height))
                size = (int(math.floor(width * scale)),
                        int(math.floor(height * scale)))
                yield image.resize(size, resample=Image.ANTIALIAS)
