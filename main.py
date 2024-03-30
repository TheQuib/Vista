#!/usr/bin/python
import drawImage

def main(debug: bool):
    values = drawImage.GatherValues(debug)

    drawImage.DrawImage(values.todays_date, values.lastUpdated_dateTime, values.planPercentRemaining, values.bonusPercentRemaining, values.random_fact, values.web_address)

if __name__ == "__main__":
    main(debug=True)