import os
import requests
import json
import csv
import time
import logging
from dotenv import load_dotenv
from time import sleep
from selenium import webdriver
from random import randint
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
from selenium.common.exceptions import NoSuchElementException

# Load environment variables from the .env file
load_dotenv()

# Retrieve the environment variables
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
orders_list = os.getenv("CSV_FILE")
wp_url = os.getenv("WP_URL")
cp_file = os.getenv("CHECKPOINT_FILE")
log_file = os.getenv("LOG_FILE")

# Configure logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#WP URL
#wp_url = wp_url
admin_url = wp_url + "/wp-admin"

# WebDriver option setup
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)


##### Selenium tasks ####
# Open the WordPress admin login page
driver.get(admin_url)

# Log an informational message
logging.info(f"Open wp admin: {admin_url}")

# Login wp-admin
driver.find_element(By.NAME,"log").send_keys(username)
driver.find_element(By.NAME,"pwd").send_keys(password)

# Log an informational message
logging.info(f"Entered username: {username}")

# Login submit
driver.find_element(By.XPATH, "//input[@type='submit']").click()

# Log an informational message
logging.info(f"Logged in")

# Delay between 10-15 second before proceed next action
sleep(randint(10,15)) # Let the user actually see something!

# Store relevant session data (e.g., cookies or tokens)
cookies = driver.get_cookies()


driver.quit()  # Close the driver

# Store the session data to be passed to the main test script
session_data = {
    "cookies": cookies,
    # Additional session data as needed
}

# Output the session data as JSON
ss_data = print(json.dumps(session_data))

# Log an informational message
logging.info(f"Session Data: {ss_data}")