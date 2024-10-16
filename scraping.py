from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import time
import csv

# Path to the correct Chrome binary
chrome_binary_path = r'C:/Program Files/Google/Chrome/Application/chrome.exe'

# Set Chrome options
options = webdriver.ChromeOptions()
options.binary_location = chrome_binary_path
options.add_argument('--headless')  # Optional, for headless browsing
options.add_argument("--disable-blink-features=AutomationControlled")  # Prevents detection of automation

# Path to ChromeDriver (update this path)
chrome_driver_path = r'C:/Users/ayush/Downloads/Selenium/chromedriver-win64/chromedriver.exe'

# Set up the service with ChromeDriver
chrome_service = Service(chrome_driver_path)

# Start ChromeDriver with options
driver = webdriver.Chrome(service=chrome_service, options=options)

# Selenium stealth settings to avoid detection
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

# Navigate to the Bloomberg Billionaire Index
url = 'https://www.bloomberg.com/billionaires/'
driver.get(url)

# Wait for the page to load
time.sleep(10)  # Increase wait time to ensure the page is fully loaded

# Get the HTML content of the page
html_content = driver.page_source

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Define lists to store the extracted data
billionaire_data = []

# Locate billionaire rows and extract required information
billionaire_rows = soup.find_all('div', class_='table-row')  # Adjust this class as necessary

# Loop through each row and extract relevant data
for row in billionaire_rows:
    rank = row.find('div', class_='t-rank').text.strip()  # Extract rank
    name = row.find('div', class_='t-name').text.strip()  # Extract name
    net_worth = row.find('div', class_='t-nw').text.strip()  # Extract net worth
    last_change = row.find('div', class_='t-lcd').text.strip()  # Extract last change
    ytd_change = row.find('div', class_='t-ycd').text.strip()  # Extract YTD change
    country = row.find('div', class_='t-country').text.strip()  # Extract country/region
    industry = row.find('div', class_='t-industry').text.strip()  # Extract industry

    # Append extracted data to the list
    billionaire_data.append([rank, name, net_worth, last_change, ytd_change, country, industry])

# Write data to a CSV file
csv_file = 'billionaire_data.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Rank', 'Name', 'Total Net Worth', 'Last Change', 'YTD Change', 'Country/Region', 'Industry'])
    # Write the data rows
    writer.writerows(billionaire_data)

print(f'Data successfully written to {csv_file}')

# Close the driver
driver.quit()