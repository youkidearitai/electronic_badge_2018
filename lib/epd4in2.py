#
# epd4in2.py for python3
#
# Original epd4in2.py was not support python3.
# This is port for python3.
#
# LICENSE :
#
# Copyright (C) Aug 4 2018, Junichi Ishida <uzulla@himitsukichi.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
#  the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

#
# You can download the original files from here.
# https://www.waveshare.com/wiki/File:4.2inch_e-paper_module_code.7z
# and documents.
# https://www.waveshare.com/wiki/4.2inch_e-Paper_Module
#
# Original's license
##
#  @filename   :   epd4in2.py
#  @brief      :   Implements for e-paper library
#  @author     :   Yehui from Waveshare
#
#  Copyright (C) Waveshare     September 9 2017
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import epdif
from PIL import Image

import RPi.GPIO as GPIO

# Display resolution
EPD_WIDTH = 400
EPD_HEIGHT = 300

# GDEW042T2 commands
PANEL_SETTING = 0x00
POWER_SETTING = 0x01
POWER_OFF = 0x02
POWER_OFF_SEQUENCE_SETTING = 0x03
POWER_ON = 0x04
POWER_ON_MEASURE = 0x05
BOOSTER_SOFT_START = 0x06
DEEP_SLEEP = 0x07
DATA_START_TRANSMISSION_1 = 0x10
DATA_STOP = 0x11
DISPLAY_REFRESH = 0x12
DATA_START_TRANSMISSION_2 = 0x13
LUT_FOR_VCOM = 0x20
LUT_WHITE_TO_WHITE = 0x21
LUT_BLACK_TO_WHITE = 0x22
LUT_WHITE_TO_BLACK = 0x23
LUT_BLACK_TO_BLACK = 0x24
PLL_CONTROL = 0x30
TEMPERATURE_SENSOR_COMMAND = 0x40
TEMPERATURE_SENSOR_SELECTION = 0x41
TEMPERATURE_SENSOR_WRITE = 0x42
TEMPERATURE_SENSOR_READ = 0x43
VCOM_AND_DATA_INTERVAL_SETTING = 0x50
LOW_POWER_DETECTION = 0x51
TCON_SETTING = 0x60
RESOLUTION_SETTING = 0x61
GSST_SETTING = 0x65
GET_STATUS = 0x71
AUTO_MEASUREMENT_VCOM = 0x80
READ_VCOM_VALUE = 0x81
VCM_DC_SETTING = 0x82
PARTIAL_WINDOW = 0x90
PARTIAL_IN = 0x91
PARTIAL_OUT = 0x92
PROGRAM_MODE = 0xA0
ACTIVE_PROGRAMMING = 0xA1
READ_OTP = 0xA2
POWER_SAVING = 0xE3


class EPD:
    def __init__(self):
        self.reset_pin = epdif.RST_PIN;
        self.dc_pin = epdif.DC_PIN;
        self.busy_pin = epdif.BUSY_PIN;
        self.width = EPD_WIDTH;
        self.height = EPD_HEIGHT;

    lut_vcom0 = [
        0x00, 0x17, 0x00, 0x00, 0x00, 0x02,
        0x00, 0x17, 0x17, 0x00, 0x00, 0x02,
        0x00, 0x0A, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x0E, 0x0E, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    lut_vcom0_quick = [
        0x00, 0x0E, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    lut_ww = [
        0x40, 0x17, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
        0x40, 0x0A, 0x01, 0x00, 0x00, 0x01,
        0xA0, 0x0E, 0x0E, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    lut_ww_quick = [
        0xA0, 0x0E, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    lut_bw = [
        0x40, 0x17, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
        0x40, 0x0A, 0x01, 0x00, 0x00, 0x01,
        0xA0, 0x0E, 0x0E, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    lut_bw_quick = [
        0xA0, 0x0E, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    lut_bb = [
        0x80, 0x17, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
        0x80, 0x0A, 0x01, 0x00, 0x00, 0x01,
        0x50, 0x0E, 0x0E, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    lut_bb_quick = [
        0x50, 0x0E, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    lut_wb = [
        0x80, 0x17, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
        0x80, 0x0A, 0x01, 0x00, 0x00, 0x01,
        0x50, 0x0E, 0x0E, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    lut_wb_quick = [
        0x50, 0x0E, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    lut_wb_black = [
        0x50, 0x0E, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    def digital_write(self, pin, value):
        epdif.epd_digital_write(pin, value)

    def digital_read(self, pin):
        return epdif.epd_digital_read(pin)

    def delay_ms(self, delaytime):
        epdif.epd_delay_ms(delaytime)

    def send_command(self, command):
        self.digital_write(self.dc_pin, GPIO.LOW)
        # the parameter type is list but not int
        # so use [command] instead of command
        epdif.spi_transfer([command])

    def send_data(self, data):
        self.digital_write(self.dc_pin, GPIO.HIGH)
        # the parameter type is list but not int
        # so use [data] instead of data
        epdif.spi_transfer([data])

    def init(self):
        if (epdif.epd_init() != 0):
            return -1
        self.reset()
        self.send_command(POWER_SETTING)
        self.send_data(0x03)  # VDS_EN, VDG_EN
        self.send_data(0x00)  # VCOM_HV, VGHL_LV[1], VGHL_LV[0]
        self.send_data(0x2b)  # VDH
        self.send_data(0x2b)  # VDL
        self.send_data(0xff)  # VDHR
        self.send_command(BOOSTER_SOFT_START)
        self.send_data(0x17)
        self.send_data(0x17)
        self.send_data(0x17)  # 07 0f 17 1f 27 2F 37 2f
        self.send_command(POWER_ON)
        self.wait_until_idle()
        self.send_command(PANEL_SETTING)
        #self.send_data(0xbf)  # KW-BF   KWR-AF  BWROTP 0f
        #self.send_data(0x0b)
        self.send_data(0x3f)
        self.send_command(PLL_CONTROL)
        self.send_data(0x3c)  # 3A 100HZ   29 150Hz 39 200HZ  31 171HZ
        return 0

    def wait_until_idle(self):
        while (self.digital_read(self.busy_pin) == 0):  # 0: busy, 1: idle
            self.delay_ms(100)

    def reset(self):
        self.digital_write(self.reset_pin, GPIO.LOW)  # module reset
        self.delay_ms(200)
        self.digital_write(self.reset_pin, GPIO.HIGH)
        self.delay_ms(200)

    def set_lut(self):
        self.send_command(LUT_FOR_VCOM)  # vcom
        for count in range(0, 44):
            self.send_data(self.lut_vcom0[count])

        self.send_command(LUT_WHITE_TO_WHITE)  # ww --
        for count in range(0, 42):
            self.send_data(self.lut_ww[count])

        self.send_command(LUT_BLACK_TO_WHITE)  # bw r
        for count in range(0, 42):
            self.send_data(self.lut_bw[count])

        self.send_command(LUT_WHITE_TO_BLACK)  # wb w
        for count in range(0, 42):
            self.send_data(self.lut_bb[count])

        self.send_command(LUT_BLACK_TO_BLACK)  # bb b
        for count in range(0, 42):
            self.send_data(self.lut_wb[count])

    def set_lut_quick(self):
        self.send_command(LUT_FOR_VCOM)  # vcom
        for count in range(0, 44):
            self.send_data(self.lut_vcom0_quick[count])

        self.send_command(LUT_WHITE_TO_WHITE)  # ww --
        for count in range(0, 42):
            self.send_data(self.lut_ww_quick[count])

        self.send_command(LUT_BLACK_TO_WHITE)  # bw r
        for count in range(0, 42):
            self.send_data(self.lut_bw_quick[count])

        self.send_command(LUT_WHITE_TO_BLACK)  # wb w
        for count in range(0, 42):
            self.send_data(self.lut_bb_quick[count])

        self.send_command(LUT_BLACK_TO_BLACK)  # bb b
        for count in range(0, 42):
            self.send_data(self.lut_wb_quick[count])

    def get_frame_buffer(self, image):
        buf = [0] * int(self.width * self.height / 8)
        # Set buffer to value of Python Imaging Library image.
        # Image must be in mode 1.
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).'.format(self.width, self.height))

        pixels = image_monocolor.load()
        for y in range(self.height):
            for x in range(self.width):
                # Set the bits for the column of pixels at the current position.
                if pixels[x, y] != 0:
                    buf[int((x + y * self.width) / 8)] |= 0x80 >> (x % 8)
        return buf

    def get_partial_frame_buffer(self, image):
        buf = [0] * int(image.size[0] * image.size[1] / 8)
        # Set buffer to value of Python Imaging Library image.
        # Image must be in mode 1.
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size

        pixels = image_monocolor.load()
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                # Set the bits for the column of pixels at the current position.
                if pixels[x, y] != 0:
                    buf[int((x + y * image.size[0]) / 8)] |= 0x80 >> (x % 8)
        return buf

    def display_frame(self, frame_buffer):
        self.send_command(RESOLUTION_SETTING)
        self.send_data(self.width >> 8)
        self.send_data(self.width & 0xff)
        self.send_data(self.height >> 8)
        self.send_data(self.height & 0xff)

        self.send_command(VCM_DC_SETTING)
        self.send_data(0x12)

        self.send_command(VCOM_AND_DATA_INTERVAL_SETTING)
        self.send_command(0x97)  # VBDF 17|D7 VBDW 97  VBDB 57  VBDF F7  VBDW 77  VBDB 37  VBDR B7

        if (frame_buffer != None):
            self.send_command(DATA_START_TRANSMISSION_1)
            for i in range(0, int(self.width * self.height / 8)):
                self.send_data(0xFF)  # bit set: white, bit reset: black
            self.delay_ms(2)
            self.send_command(DATA_START_TRANSMISSION_2)
            for i in range(0, int(self.width * self.height / 8)):
                self.send_data(frame_buffer[i])
            self.delay_ms(2)

        self.set_lut()

        self.send_command(DISPLAY_REFRESH)
        self.delay_ms(100)
        self.wait_until_idle()

    def set_partial_window(self, buffer_black, x, y, w, l, dtm):
        self.send_command(PARTIAL_IN)
        self.send_command(PARTIAL_WINDOW)
        self.send_data(x >> 8) # HRST[8]
        self.send_data(x & 0xf8) # HRST[7:3]
        self.send_data(((x & 0xf8) + w - 1) >> 8) # HRED[8]
        self.send_data(((x & 0xf8) + w - 1) | 0x07) # HRED[7:3]
        self.send_data(y >> 8) # VRST[8]
        self.send_data(y & 0xff) # VRST[7:0]
        self.send_data((y + l - 1) >> 8) # VRED[8]
        self.send_data((y + l - 1) & 0xff)# VRED[7:0]
        self.send_data(0x01) # PT_SCAN
        if (dtm == 1):
            self.send_command(DATA_START_TRANSMISSION_1)
        else:
            self.send_command(DATA_START_TRANSMISSION_2)

        if (buffer_black is not None):
            for i in range(0, int(w / 8 * l)):
                self.send_data(buffer_black[i])
        else:
            for i in range(0, int(w / 8 * l)):
                self.send_data(0x00)

        self.send_command(PARTIAL_OUT)
        self.set_lut_quick()
        self.send_command(DISPLAY_REFRESH)
        self.wait_until_idle()

    ##
    #  @brief: After this command is transmitted, the chip would enter the
    #          deep-sleep mode to save power.
    #          The deep sleep mode would return to standby by hardware reset.
    #          The only one parameter is a check code, the command would be
    #          executed if check code = 0xA5.
    #          You can use reset() to awaken or init() to initialize
    ##
    def sleep(self):
        self.send_command(VCOM_AND_DATA_INTERVAL_SETTING)
        self.send_data(0x17)  # border floating
        self.send_command(VCM_DC_SETTING)  # VCOM to 0V
        self.send_command(PANEL_SETTING)  #
        self.delay_ms(100)

        self.send_command(POWER_SETTING)  # VG&VS to 0V fast
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.delay_ms(100)

        self.send_command(POWER_OFF)  # power off
        self.wait_until_idle()
        self.send_command(DEEP_SLEEP)  # deep sleep
        self.send_data(0xA5)

### END OF FILE ###
