import requests
from bs4 import BeautifulSoup
#from inky import InkyPHAT

# Send a web request to the web interface
url = 'http://192.168.0.1'
page = requests.get(url)

# Parse the HTML response
parser = BeautifulSoup(page.content, 'html.parser')

divs = parser.findAll('div', attrs={'class':'col-md-6'})

print(divs)

# Display data on the e-ink display
#inky_display = InkyPHAT('red')
#inky_display.set_border(inky_display.WHITE)
#for row in rows:
#    inky_display.text((0, 0), row.get_text(), inky_display.RED)
#    inky_display.show()