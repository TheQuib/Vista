import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument('-headless')
driver = webdriver.Firefox(options=options)

driver.get('http://192.168.0.1')

time.sleep(5)

data = driver.page_source

driver.quit()

#print(data)

parser = BeautifulSoup(data, 'html.parser')

# Find all divs with the class "text-center copyright_grey"
divs = parser.find_all('div', {'class': 'text-center copyright_grey'})

# List to hold the numbers
numbers = []

# For each div, get the text within it
for div in divs:
    text = ' '.join(div.stripped_strings)
    parts = text.split()  # split the text into parts
    number = parts[0]  # the first part is the number (as a string)
    numbers.append(number)  # add the number to the list

# Access the numbers
planTotal = numbers[0]
planRemaining = numbers[1]
bonusTotal = numbers[2]
bonusRemaining = numbers[3]

# Calculate percentages
planPercentRemaining = f"{float(planRemaining)/float(planTotal):.2%}"
bonusPercentRemaining = f"{float(bonusRemaining)/float(bonusTotal):.2%}"

print("Total in plan: " + planTotal)
print("Remaining in plan: " + planRemaining )
print("Plan percent left: " + planPercentRemaining + "\n")

print("Total in bonus: " + bonusTotal)
print("Remaining in bonus: " + bonusRemaining)
print("Bonus percent left: " + bonusPercentRemaining + "\n")