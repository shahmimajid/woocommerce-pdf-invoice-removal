import os
import requests
import csv
import time
import logging
from dotenv import load_dotenv
from time import sleep
from selenium import webdriver
from random import randint
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
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

# File path for storing the last processed line number
checkpoint_file = cp_file

#WP url
#base_url = "https://www.e-renew.my/wp-admin/post.php?post={}&action=edit"
wp_url = wp_url
admin_url = wp_url + "/wp-admin"
order_url = wp_url + "/wp-admin/post.php?post={}&action=edit"

# WebDriver option setup
chrome_options = Options()
chrome_options.add_argument("--headless")
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

# Delay between 3-6 second before proceed next action
sleep(randint(4,7)) # Let the user actually see something!


# Check if the checkpoint file exists
if os.path.exists(cp_file):
    with open(cp_file, "r") as file:
        last_processed_line = int(file.read())
else:
    last_processed_line = 0

# Open the input data file
with open(orders_list, "r") as file:
    # Loop through the remaining lines
    for line_number, line in enumerate(file, start=1):
        # Skip the lines that have already been processed
        if line_number <= last_processed_line:
            continue

        # Process the line data
        line = line.strip()

        try:

            # Construct the URL or perform other actions based on the line data
            url = order_url.format(line)

            # Measure time taken for each order
            start_time = time.time()

            # Send a HEAD request to check the response status code
            response = requests.head(url)

            # Check if the response code is 302 (OK)
            if response.status_code == 302:
                # Navigate to the URL using Selenium
                driver.get(url)
                print(f"Order no: {line}")
                # Show Order no processed
                logging.info("Order ID : %s", line)

                try:
                    # get element
                    element = driver.find_element(By.XPATH, "//a[@class='wcj_need_confirmation' and text()='Delete']")

                    # Get the href value
                    href = element.get_attribute("href")
                    print(f"Found element with href: {href}")

                    # Log an informational message
                    #logging.info(f"Element: {href}")

                    # Combine the relative URL with the base URL
                    full_url = urljoin(wp_url, href)

                    # Perform GET to delete pdf invoice
                    driver.get(full_url)
                    logging.info("Performed GET : %s ", full_url)

                    end_time = time.time()
                    duration = end_time - start_time
                    logging.info("Time taken to complete order: %.2f seconds", duration)


                except NoSuchElementException:
                    print("Element not found.")
                    logging.info("Element not found")
                    continue
            else:
                # Handle the error (e.g., print an error message)
                print(f"Error occurred while navigating to order id : {line}. Response code: {response.status_code}")
                logging.info(f"Error occurred while navigating to order id : {line}. Response code: {response.status_code}")

        except requests.RequestException as e:
            # Handle the error (e.g., print an error message)
            print(f"Error occurred while sending request to order {line}: {str(e)}")
            logging.info(f"Error occurred while sending request to order {line}: {str(e)}")

        # Update the checkpoint file with the current line number
        with open(cp_file, "w") as checkpoint:
            checkpoint.write(str(line_number))












#---------
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

# Delay between 3-6 second before proceed next action
sleep(randint(4,7)) # Let the user actually see something!

# Check if the checkpoint file exists
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, "r") as file:
        last_processed_line = int(file.read())
else:
    last_processed_line = 0

# Open the input data file
with open(orders_list, "r") as file:
    # Skip the lines that have already been processed
    for _ in range(last_processed_line):
        next(file)

    # Loop through the remaining lines
    for line_number, line in enumerate(file, start=last_processed_line + 1):
        # Process the line data
        line = line.strip()
        # ...

        try:
            # Construct the URL or perform other actions based on the line data
            url = order_url.format(line)

            # Send a HEAD request to check the response status code
            response = requests.head(url)

            # Check if the response code is 302 (OK)
            if response.status_code == 302:
                # Navigate to the URL using Selenium
                driver.get(url)
                print(f"Order no: {line}")
                #Show Order no processed
                logging.info("Order ID : %s", line)

                try:
                    # get element
                    element = driver.find_element(By.XPATH, "//a[@class='wcj_need_confirmation' and text()='Delete']")

                    # Get the href value
                    href = element.get_attribute("href")
                    print(f"Found element with href: {href}")

                    # Log an informational message
                    logging.info(f"Element: {href}")

                    # Combine the relative URL with the base URL
                    full_url = urljoin(wp_url, href)

                    #Perform GET to delete pdf invoice
                    driver.get(full_url)
                    logging.info("URL is %s ", full_url)

                except NoSuchElementException:
                    print("Element not found.")
                    logging.info("Element not found")
                    continue
            else:
                # Handle the error (e.g., print an error message)
                print(f"Error occurred while navigating to order id : {line}. Response code: {response.status_code}")
                # Continue to the next iteration
                continue

        except requests.RequestException as e:
            # Handle the error (e.g., print an error message)
            print(f"Error occurred while sending request to order {line}: {str(e)}")
            logging.info("Error {str(e)}")

            # Continue to the next iteration
            continue