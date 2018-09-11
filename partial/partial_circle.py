#!/usr/bin/python3.5
#
# Usage:
# $ python parcial_circle.py
#

import os
import sys

import time
import picamera
import io
from PIL import Image, ImageDraw
import math

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../lib'))

import epd4in2
from nafuda import Nafuda

def main():
    nafuda = Nafuda()
    fullFlush = Image.new("RGB", (400, 300), "#FFFFFF")
    draw = ImageDraw.Draw(fullFlush)

    nafuda.draw_image_buffer(fullFlush)

    images = []
    for i in range(0, 16):
        image = Image.new("RGB", (80, 60), "#FFFFFF")
        draw = ImageDraw.Draw(image)
        x = 30 + int(20 * math.sin(i))
        y = 20 + int(20 * math.cos(i))
        draw.rectangle(((x, y), (x + 16, y + 16)), 0)
        images.append(image)

    # Orientation 90 is vertical nafuda mode. 0 is horizontal
    for i in range(0, 16):
        nafuda.draw_partial_window(images[i], 0, 0, 80, 60, 2, orientation=0)
        nafuda.draw_partial_window(images[i], 200, 200, 80, 60, 2, orientation=0)

    nafuda.draw_image_buffer(fullFlush)

if __name__ == '__main__':
    main()
