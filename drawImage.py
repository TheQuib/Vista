#!/usr/bin/python
from src.scraper import GetHTML
from src.displayManager import DisplayManager
from src.screenControls import ScreenControls
from threading import Thread
from datetime import datetime
import random
import json
import os, logging, time
import psutil

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(
            __file__
        )
    )
)

class BootScreen:
    def __init__(self):
        logging.debug("Creating DisplayManager object")
        dm = DisplayManager()

        logging.info("Drawing boot screen")
        dm.draw_image(0, 0, 800, __location__ + '/assets/bootScreen.bmp')

        logging.info("Pushing image to E-Paper")
        dm.display_image()

class GatherValues:
    def __init__(self, debug=False):
        if debug == True:
            example = True
        else:
            example = False

        if example == True:
            with open(__location__ + '/example.html') as html:
                logging.info("Parsing example HTML to get necessary values")
                hughesnet_values = GetHTML.parse_website(html)
                #print(hughesnet_values)

        else:
            logging.info("Load HTML from website")
            html = GetHTML.load_website()
            logging.info("Parse HTML to get necessary values")
            hughesnet_values = GetHTML.parse_website(html)
            #print(hughesnet_values)


        logging.info("Calculating regular value")
        planRemaining = float(hughesnet_values['planRemaining'])
        planTotal = float(hughesnet_values['planTotal'])
        self.planPercentRemaining = round((planRemaining / planTotal) * 100, 2)
        
        logging.info("Calculating bonus value")
        bonusRemaining = float(hughesnet_values['bonusRemaining'])
        bonusTotal = float(hughesnet_values['bonusTotal'])
        self.bonusPercentRemaining = round((bonusRemaining / bonusTotal) * 100, 2)

        logging.info("Getting IP Address of device")
        address = psutil.net_if_addrs()
        self.local_ip = address['wlan0'][0].address
        self.web_address = 'http://' + self.local_ip + ':5000'

        logging.info("Getting current date and formatting")
        current_dateTime = datetime.now()
        self.todays_date = current_dateTime.strftime('%A, %B %d')
        self.lastUpdated_dateTime = current_dateTime.strftime('%m/%d/%y %I:%M %p')

        logging.info("Getting facts from JSON file and selecting random fact")
        with open(__location__ + '/facts.json', 'r') as factsFile:
            facts = json.load(factsFile)
        self.random_fact = random.choice(facts)
        

class DrawImage:
    def __init__(self, todays_date, lastUpdated_dateTime, planPercentRemaining, bonusPercentRemaining, random_fact, web_address):
        logging.debug("Creating DisplayManager object")
        dm = DisplayManager()

        logging.info("Begin drawing")
        logging.info("Drawing header")
        dm.draw_text("Vista", 10, 4, 32)
        dm.draw_image(10, 11, 112, __location__ + '/assets/vista.bmp')
        dm.draw_text("github.com/TheQuib/Vista", 10, 44, 16)
        dm.draw_text(todays_date, 511, 4, 32, align='right', right_edge=800, right_margin=10)
        dm.draw_text("Last updated " + lastUpdated_dateTime, 0, 43, 16, align='right', right_edge=800, right_margin=10)
        dm.draw_line((0,70), (800, 70), width=3)

        logging.info("Drawing regular plan block")
        dm.draw_box((10, 84), (395, 215), 10)
        dm.draw_text("Regular plan", 25, 93, 24, __location__ + '/src/font/Asap/static/Asap-SemiBold.ttf')
        dm.draw_progress_bar(planPercentRemaining, 25, 133, 355, 35)
        dm.draw_text(str(planPercentRemaining) + "% remaining", 25, 172, 20)

        logging.info("Drawing bonus plan block")
        dm.draw_box((405, 84), (790, 215), 10)
        dm.draw_text("Bonus plan", 420, 93, 24, __location__ + '/src/font/Asap/static/Asap-SemiBold.ttf')
        dm.draw_progress_bar(bonusPercentRemaining, 420, 133, 355, 35)
        dm.draw_text(str(bonusPercentRemaining) + "% remaining", 420, 172, 20)

        logging.info("Drawing time left in cycle block")
        dm.draw_box((10, 225), (395,356), 10)
        dm.draw_text("Time left in cycle", 25, 234, 24, __location__ + '/src/font/Asap/static/Asap-SemiBold.ttf')
        dm.draw_progress_bar(25, 25, 274, 355, 35)
        dm.draw_text(str(25) + " days remaining", 25, 313, 20)

        logging.info("Drawing fun fact block")
        dm.draw_box((405, 225), (790, 356), 10)
        dm.draw_text("Fun fact", 420, 234, 24, __location__ + '/src/font/Asap/static/Asap-SemiBold.ttf')
        dm.draw_multiline_text(random_fact, 420, 270, 24)

        logging.info("Drawing footer")
        dm.draw_image(10, 370, 304, __location__ + '/assets/theCabin.bmp')
        dm.draw_text("Manage this display:", 497, 447, 20)
        dm.draw_qr_code(690, 370, 100, web_address)


        logging.info("Pushing image to E-Paper")
        dm.display_image()