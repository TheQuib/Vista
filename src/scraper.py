import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import logging

class GetHtml:
    def load_website():
        options = Options()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)
        logging.debug("Set web driver")

        logging.debug("Load web page")
        driver.get('http://192.168.0.1')

        logging.debug("Waiting for 5 seconds to make sure all scripts are run")
        time.sleep(5)

        logging.debug("Setting html variable")
        html = driver.page_source

        logging.debug("Exiting driver")
        driver.quit()

        return html

        # Print data for debugging purposes
        #print(data)

    def parse_website(html):
        parser = BeautifulSoup(html, 'html.parser')

        logging.debug("Getting divs")
        divs = parser.find_all('div', {'class': 'text-center copyright_grey'})

        logging.debug("Create list for number storage")
        numbers = []

        logging.debug("Splitting text from divs")
        for div in divs:
            text = ' '.join(div.stripped_strings)
            parts = text.split()
            number = parts[0]
            numbers.append(number)

        logging.debug("Accessing numbers")
        planTotal = numbers[0]
        planRemaining = numbers[1]
        bonusTotal = numbers[2]
        bonusRemaining = numbers[3]

        logging.debug("Calculating percentages")
        planPercentRemaining = f"{float(planRemaining)/float(planTotal):.2%}"
        bonusPercentRemaining = f"{float(bonusRemaining)/float(bonusTotal):.2%}"

        logging.debug("Returning list of values")
        values = {'planTotal': planTotal,
                  'planRemaining': planRemaining,
                  'planPercentageRemaining': planPercentRemaining,
                  'bonusTotal': bonusTotal,
                  'bonusRemaining': bonusRemaining,
                  'bonusPercentRemaining': bonusPercentRemaining
                }

        return values

        # Print all values for deb
        #print("Total in plan: " + planTotal)
        #print("Remaining in plan: " + planRemaining )
        #print("Plan percent left: " + planPercentRemaining + "\n")

        #print("Total in bonus: " + bonusTotal)
        #print("Remaining in bonus: " + bonusRemaining)
        #print("Bonus percent left: " + bonusPercentRemaining + "\n")