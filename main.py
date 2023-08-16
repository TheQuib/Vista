#!/usr/bin/python
from src.scraper import GetHTML
#from src.progressbar import ProgressBar
from src.web import Webserver
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
        html = GetHTML.load_website
        logging.info("Parse HTML to get necessary values")
        hughesnet_values = GetHTML.parse_website(html)
        #print(hughesnet_values)
    
    web = Webserver()
    web.start_server(hughesnet_values['planTotal'], hughesnet_values['planRemaining'], hughesnet_values['bonusTotal'], hughesnet_values['bonusRemaining'])


main(useExampleHtml)