#!/usr/bin/python3
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

def progress_bar(x, y, width, height, progress, bg=(129,66,97), fg=(211,211,211), fg2=(15,15,15)):
    Himage = Image.new('1', (width, height), 255)
    draw = ImageDraw.Draw(Himage)
    # Draw the background
    draw.rectangle((x+(height/2), y, x+width+(height/2), y+height))#, fill=fg2, width=10)
    draw.ellipse((x+width, y, x+height+width, y+height))#, fill=fg2)
    draw.ellipse((x, y, x+height, y+height))#, fill=fg2)
    width = int(width*progress)
    # Draw the part of the progress bar that is actually filled
    draw.rectangle((x+(height/2), y, x+width+(height/2), y+height))#, fill=fg, width=10)
    draw.ellipse((x+width, y, x+height+width, y+height))#, fill=fg)
    draw.ellipse((x, y, x+height, y+height))#, fill=fg)
    return(Himage)

try:
    logging.info("epd7in5_V2 Test")
    epd = epd7in5_V2.EPD()

    logging.info("Initialize and Clear")
    epd.init()
    epd.Clear()

    logging.info("Draw progress bar")
    bar = progress_bar(10, 10, epd.width, epd.height, 0.25)
    epd.display(epd.getbuffer(bar))

    logging.info("Set display to sleep")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()