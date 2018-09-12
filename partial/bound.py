#!/usr/bin/python3.5
#
# バウンドするサンプル

# Usage:
# $ python bound.py
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

    x = 4
    y = 4
    movex = 1
    movey = 1
    for i in range(0, 120):
        image = Image.new("RGB", (400, 300), "#FFFFFF")
        draw = ImageDraw.Draw(image)
        draw.rectangle(((x, y), (x + 16, y + 16)), 0)

        nafuda.draw_partial_window(nafuda.get_partial_frame_buffer(image), 0, 0, 400, 300, 2, orientation=0)

        if x < 0 or x >= epd4in2.EPD_WIDTH - 16:
            movex *= -1
        if y < 0 or y >= epd4in2.EPD_HEIGHT - 16:
            movey *= -1 

        x += 10 * movex
        y += 10 * movey

    nafuda.draw_image_buffer(fullFlush)

if __name__ == '__main__':
    main()

