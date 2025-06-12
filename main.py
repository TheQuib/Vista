#!/usr/bin/python
import drawImage
import json
import os

def main(debug: bool):
    values = drawImage.GatherValues(debug)

    drawImage.DrawImage(values.todays_date, values.lastUpdated_dateTime, values.planPercentRemaining, values.bonusPercentRemaining, values.random_fact, values.web_address)

    data = {
        'plan_total': values.planTotal,
        'plan_remaining': values.planRemaining,
        'bonus_total': values.bonusTotal,
        'bonus_remaining': values.bonusRemaining,
        'plan_percentage': values.planPercentRemaining,
        'bonus_percentage': values.bonusPercentRemaining,
        'fun_fact': values.random_fact
    }
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'latest_data.json')
    with open(data_path, 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    main(debug=True)