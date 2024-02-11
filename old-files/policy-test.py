from selenium import webdriver
import random
import time
import json
import json
import random
import string
from datetime import datetime, timedelta
import requests
import argparse
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from  selenium.webdriver.chrome.options import Options
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.ui import WebElement

chrome_options = Options()
chrome_options.add_experimental_option("detach",True)
# Configuration loading function
def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

config = load_config()
# Define the path to the JSON file
json_file_path = "products/AutoInsurance/policy/policy.json"

# Read the JSON file
with open(json_file_path, "r") as json_file:
    policy_data = json.load(json_file)

# Now, you can access and manipulate the data in the 'policy_data' dictionary
# For example, to print the 'fields' key from your provided JSON structure:
print(policy_data["fields"])



def login_to_socotra(username, password, hostname):
    driver = webdriver.Chrome(options=chrome_options)
    login_url = config['login_url']
    driver.get(login_url)
    time.sleep(5) 

    driver.find_element(By.ID, "LoginForm__UsernameField--Standard").send_keys(username) 
    driver.find_element(By.ID, "LoginForm__PasswordField--Standard").send_keys(password) 
    driver.find_element(By.ID, "LoginForm__HostnameField--Standard").send_keys(hostname) 
    driver.find_element(By.ID, "LoginForm__Button--StandardLogin").click()
    time.sleep(5) 

    return driver

def create_session_and_login(hostname):
    username = config['username']
    password = config['password']
    hostname = config['hostname']
    sandbox_url = config['sandbox_url']

    session = requests.Session()
    response = requests.post(
        f'{sandbox_url}/account/authenticate',
        json = { 'hostName':hostname,
                 'username':username,
                 'password':password})

session = create_session_and_login(config['hostname'])
driver = login_to_socotra(config['username'], config['password'], config['hostname'])
locator_url = 'https://sandbox.socotra.com/policy/100000810/quotes/100000816/details'

# Load the webpage where the UI elements are located
# driver.get("https://sandbox.socotra.com/policy/100000810/quotes/100000816/details")
driver.get(locator_url)


# Function to select a random value from a list of values
def select_random_value(values):
    return random.choice(values)

# Loop through the fields and interact with the UI elements
for field in fields_json["fields"]:
    field_name = field["name"]
    field_type = field["type"]

    if field_type == "select":
        # Find the select element and select a random option
        select_element = driver.find_element_by_name(field_name)
        options = select_element.find_elements_by_tag_name("option")
        random_option = select_random_value(options)
        random_option.click()

    elif field_type == "string":
        # Find the input element and enter a random string value
        input_element = driver.find_element_by_name(field_name)
        random_string = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(8))
        input_element.send_keys(random_string)

    # Add more conditions for other field types (e.g., number, checkbox) as needed

    # Sleep for a moment to simulate user interaction
    time.sleep(2)

# Close the WebDriver when done
driver.quit()
