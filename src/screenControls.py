#!/usr/bin/python
# -*- coding:utf-8 -*-
# Clears the display

import logging

from . import epd7in5_V2

logging.basicConfig(level=logging.DEBUG)

class ScreenControls:
    def clearScreen():
        try:
            logging.info("epd7in5_V2 Test")
            epd = epd7in5_V2.EPD()

            logging.info("Initialize and Clear")
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