#!/usr/bin/python
from src.scraper import GetHTML
from src.displayManager import DisplayManager
from src.screenControls import ScreenControls
from src.web import Webserver
from threading import Thread
import os, logging, time


useExampleHtml = True

def main(example):
    if example == True:
        with open('example.html') as html:
            logging.info("Parsing example HTML to get necessary values")
            hughesnet_values = GetHTML.parse_website(html)
            #print(hughesnet_values)

    else:
        logging.info("Load HTML from website")
        html = GetHTML.load_website()
        logging.info("Parse HTML to get necessary values")
        hughesnet_values = GetHTML.parse_website(html)
        #print(hughesnet_values)
    
    # Start web server process
    web = Webserver(clear_display=ScreenControls.clearScreen())
    web_thread = Thread(target=web.start_server, args=(hughesnet_values['planTotal'], hughesnet_values['planRemaining'], hughesnet_values['bonusTotal'], hughesnet_values['bonusRemaining']))
    web_thread.daemon = True
    web_thread.start()
   
    # Calculate percentage
    planRemaining = float(hughesnet_values['planRemaining'])
    planTotal = float(hughesnet_values['planTotal'])
    planPercentRemaining = round((planRemaining / planTotal) * 100, 2)
    # Display progress bar on display
    dm = DisplayManager()
    dm.draw_progress_bar(planPercentRemaining, 75, 50, 300, 40)
    dm.display_image()

    # Wait 1 minute (dev purposes)
    time.sleep(60)
    web.stop_server()
    web_thread.join()


main(useExampleHtml)