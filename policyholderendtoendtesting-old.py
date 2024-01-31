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

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_email():
    return f"{random_string(7)}@example.com"

def random_phone_number():
    return f"+1{random.randint(1000000000, 9999999999)}"

def random_date_of_birth():
    start_date = datetime(1940, 1, 1)
    end_date = datetime(2003, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return (start_date + timedelta(days=random_number_of_days)).strftime("%Y-%m-%d")

def generate_data(name):
    if name == "email":
        return random_email()
    elif name == "phone_number":
        return random_phone_number()
    elif name == "date_of_birth":
        return random_date_of_birth()
    elif name == "ofac_outcome":
        return random.choice(["approved", "step up"])
    else:
        return random_string()

def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def extract_fields(data):
    fields = []
    for page in data["pages"]:
        for section in page["sections"]:
            for field in section["fields"]:
                fields.append(field["name"])
    return fields

def datagen():
    fields = extract_fields(load_json(config['policyholder_form_json']))
    all_data = []
    for _ in range(config['num_records']):
        record = {
            "values": {field: generate_data(field) for field in fields},
            "completed": True
        }
        all_data.append(record)
    return all_data

def get_hostname():
    parser = argparse.ArgumentParser()
    parser.add_argument('hostname')
    args = parser.parse_args()
    return args.hostname

def create_multiple_policyholders(session, num_policyholders):
    sandbox_url = config['sandbox_url']
    policyholder_information_list = []
    policyholder_values_list = datagen()
    print("policyholder_values_list", policyholder_values_list)

    for policyholder_values in policyholder_values_list[:num_policyholders]:
        if isinstance(policyholder_values, dict) and 'values' in policyholder_values:
            correct_structure = {
                "values": policyholder_values['values'],
                "completed": True
            }

            response = session.post(f'{sandbox_url}/policyholder/create', json=correct_structure)
            policyholder_information = response.json()
            policyholder_information_list.append(policyholder_information)
        else:
            print(f'Invalid policyholder structure: {policyholder_values}')

    print(f'Created {len(policyholder_information_list)} policyholders')
    return policyholder_information_list

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

    authorization_token = response.json()['authorizationToken']
    session.headers.update({'Authorization': authorization_token})
    return session

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

def is_date_format(value):
    return bool(re.match(r'\d{4}-\d{2}-\d{2}', value))

def format_date(value):
    return value.replace('-', '/') if value else value


# def policytesting():
#     # Fetch fields from json and load data to policyholder form
#     with open('policyholder/policyholder.form.json', 'r') as file:
#         data = json.load(file)
#     # Extract field names from json
#     names_to_check = []
#     for page in data['pages']:
#         for section in page['sections']:
#             for field in section['fields']:
#                 names_to_check.append(field['name'])

def main():
    
    session = create_session_and_login(config['hostname'])
    driver = login_to_socotra(config['username'], config['password'], config['hostname'])
    locator_url = config['locator_url']
    
    # Fetch fields from json and load data to policyholder form
    with open('policyholder/policyholder.form.json', 'r') as file:
        data = json.load(file)

    # Extract field names from json
    names_to_check = []
    for page in data['pages']:
        for section in page['sections']:
            for field in section['fields']:
                names_to_check.append(field['name'])

    num_policyholders = 2

    policyholder_information_list = create_multiple_policyholders(session, num_policyholders)
    print("policyholder_information_list", policyholder_information_list)
    
    test_results = []
    api_data = []  # To capture policy locator details along with API data


    for idx, policy_info in enumerate(policyholder_information_list):
        policy_locator = policy_info['locator']

                # Capture policy locator details
        api_data_entry = {
            "Policy Locator": policy_locator,
            "Data": policy_info['entity']['values']
        }
        api_data.append(api_data_entry)
        
        url = f"{locator_url}/policyholder/{policy_locator}"
        print("url: ", url)
        
        driver.get(url)
        time.sleep(5)
        try:
            start_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/main/div/div[1]/div/a"))
            )
            start_button.click()
            print("Start button clicked successfully.")
        except Exception as e:
            print(f"Failed to click start button: {str(e)}")


        # startbutton.click()
        try:
        #checking if  new application form is loaded
            startApplication_check = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/div[1]/div[2]/div/div/div[1]/div/div")))
        except:
            driver.quit() 
        #dropdown menu element selection and click
        dropdown1 = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div/div")
        dropdown1.click()
        try:
            #checking if the dropdown is activated
            Dummy_check = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/div[4]/div[3]/ul/li[1]")))
        except:
            driver.quit() 
            # select = Select(driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div/div"))
            # select.select_by_visible_text('Auto Insurance')

            # dropdown1 = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div/div")
            # dropdown1.click()
            
            # Auto Insurance selected
        driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/ul/li[1]").click()
        # dropdownbutton = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div/div")
        #select and click the create button
        driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div[3]/button[2]").click()
        

        # var_felony= driver.find_element(By.ID,'policyForm.10_year_felony_conviction').value
        var_felony= driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[9]/div/div/div/div/input')
        
        print("var_felony", var_felony)


        # driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/ul/li[1]").click()


        # Click on the dropdown to open it
        # dropdownbutton.click()

        # Select an option by its visible text
        # dropdownbutton.select_by_visible_text('Auto Insurance')
        
        # Locate and click on the desired item by its XPath (replace with your actual XPath)
        # item_xpath = '//*[@id="menu-"]/div[3]/ul/li[1]' # Replace with your item's XPath
        # driver.find_element(By.XPATH, item_xpath).click()

        # Wait for a short time to ensure the dropdown options are visible (you may need to adjust the wait time)
        time.sleep(2)

        # Locate and click on the specific option you want (replace with the actual XPath)
        # option = driver.find_element(By.XPATH, '//*[@id="menu-"]/div[1]')  # Replace with your actual XPath
        # option.click()
        # WebElement selectElement = driver.findElement(By.id("s");
        # Select select = new Select(selectElement);
        # Locate the dropdown element by ID (replace 'id' with the actual ID of your dropdown element)
        # dropdown = Select(driver.find_element(By.ID, 'product-select'))

        # Get all options
        # options = dropdown.options

        # Get the length
        # print(len(options))

        # Loop to print one by one
        # for option in options:
            # print(option.text)
        # Assuming you have a second dropdown to interact with, locate and select the desired option
        # element = driver.find_element(By.ID, '//*[@id="menu-"]/div[1]')  # Replace 'dropdown_id' with the actual ID of the dropdown element
        # select = Select(element)
# /html/body/div[4]/div[1]
        # Select an option by visible text
        # select.select_by_visible_text('Auto Insurance').click()
        # Locate the element with the text "Auto Insurance" using XPath
        # auto_insurance_element = driver.find_element(By.XPATH, '//*[contains(text(), "Auto Insurance")]')

        # Click on the "Auto Insurance" option
        # auto_insurance_element.click()
# /html/body/div[4]/div[3]/ul/li[1]
        # Print the text of the element (if needed)
        # print(element.text)


        input_elements = driver.find_elements(By.TAG_NAME, "input")

        for name in names_to_check:
            found = False
            for input_element in input_elements:
                input_id = input_element.get_attribute("id")
                if name in input_id:
                    found = True
                    break

            if found:
                api_value = policy_info['entity']['values'].get(name)
                if api_value:
                    api_value = api_value[0] if isinstance(api_value, list) else api_value
                    if is_date_format(api_value):
                        api_value = format_date(api_value)

                    input_field = driver.find_element(By.ID, input_id)
                    web_page_value = input_field.get_attribute("value")

                    test_result = {
                        "Field Name": name,
                        "API Value": api_value,
                        "Web Page Value": web_page_value,
                        "Match": api_value == web_page_value
                    }
                    test_results.append(test_result)
                else:
                    print(f"{name} Field is present in the page, but no API value found.")
            else:
                print(f"{name} Field is not present in the page")
    print(test_results)   


# //*[@id="app"]/div[2]/main/div/div[1]/div/a

    # driver.quit()

    # if os.path.exists('test_results.csv'):
    #     os.remove('test_results.csv')
    # with open('test_results.csv', 'a', newline='') as file:
    #     writer = csv.DictWriter(file, fieldnames=["Field Name", "API Value", "Web Page Value", "Match"])
    #     writer.writeheader()
    #     for result in test_results:
    #         writer.writerow(result)

    # print("Test results have been written to test_results.csv")

    #     # Store the API data with policy locator details in a CSV file
    # with open('api_data.csv', 'w', newline='') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=["Policy Locator", "Data"])
    #     writer.writeheader()
    #     for entry in api_data:
    #         writer.writerow(entry)


if __name__ == '__main__':
    main()