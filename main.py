#!/usr/bin/python
import drawImage

def main():
    values = drawImage.GatherValues(debug=True)

    drawImage.DrawImage(values.todays_date, values.lastUpdated_dateTime, values.planPercentRemaining, values.bonusPercentRemaining, values.random_fact, values.local_ip)

if __name__ == "__main__":
    main()