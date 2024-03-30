#!/usr/bin/python

import time
import drawImage

def boot(debug):
    values = drawImage.GatherValues(debug)

    drawImage.BootScreen()

    time.sleep(120)

    drawImage.DrawImage(values.todays_date, values.lastUpdated_dateTime, values.planPercentRemaining, values.bonusPercentRemaining, values.random_fact, values.web_address)

boot(debug=True)