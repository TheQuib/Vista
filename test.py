#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import logging
import time

import driver.epd7in5_V2 as epd7in5_V2

from PIL import Image,ImageDraw,ImageFont

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(
            __file__
        )
    )
)

picdir = __location__ + "/assets"
logging.basicConfig(level=logging.DEBUG)


try:
    logging.info("epd7in5_V2 Test")
    epd = epd7in5_V2.EPD()

    logging.info("Initialize and Clear")
    epd.init()
    epd.Clear()

    logging.info("Read '7in5_V2.bmp image")
    Himage = Image.open(os.path.join(picdir, '7in5_V2.bmp'))

    logging.info ("Display image")
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

    logging.info("Clear display")
    epd.init()
    epd.Clear()

    logging.info("Set display to sleep")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()