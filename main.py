#!/usr/bin/python
from src.scraper import GetHTML
from src.displayManager import DisplayManager
from src.screenControls import ScreenControls
from src.web import Webserver
from threading import Thread
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
   
    # Calculate percentages
    planRemaining = float(hughesnet_values['planRemaining'])
    planTotal = float(hughesnet_values['planTotal'])
    planPercentRemaining = round((planRemaining / planTotal) * 100, 2)
    bonusRemaining = float(hughesnet_values['bonusRemaining'])
    bonusTotal = float(hughesnet_values['bonusTotal'])
    bonusPercentRemaining = round((bonusRemaining / bonusTotal) * 100, 2)

    # Get IP Address of device
    address = psutil.net_if_addrs()
    local_ip = address['wlan0'][0].address

    # Display progress bar on display
    dm = DisplayManager()
    dm.draw_text("SkyStat", 70, 15, 40)
    dm.draw_text("github.com/TheQuib/SkyStat", 70, 58, 17)
    dm.draw_text("Manage this display...", 495, 445, 17)
    dm.draw_qr_code(655, 375, 100, local_ip)
    dm.draw_line((0,90), (800, 90), width=3)

    dm.draw_box((70,104), (400,220), 5)
    dm.draw_text("Regular Plan", 80, 114, 28, __location__ + '/src/font/Asap/static/Asap-SemiBold.ttf')
    dm.draw_progress_bar(planPercentRemaining, 80, 148, 300, 40)
    dm.draw_text(str(planPercentRemaining) + " remaining", 80, 188, 28)

    dm.draw_box((70,282), (400,398), 5)
    dm.draw_text("Bonus Plan", 80, 292, 28, __location__ + '/src/font/Asap/static/Asap-SemiBold.ttf')
    dm.draw_progress_bar(bonusPercentRemaining, 80, 326, 300, 40)
    dm.draw_text(str(bonusPercentRemaining) + " remaining", 80, 366, 28)

    dm.display_image()

    # Start web server process
    web = Webserver(clear_display=ScreenControls.clearScreen())
    web_thread = Thread(target=web.start_server, args=(hughesnet_values['planTotal'], hughesnet_values['planRemaining'], hughesnet_values['bonusTotal'], hughesnet_values['bonusRemaining']))
    web_thread.daemon = True
    web_thread.start()

    # Wait 1 minute (dev purposes)
    time.sleep(60)
    web.stop_server()
    web_thread.join()


main(useExampleHtml)