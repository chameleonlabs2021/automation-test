import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

import time
from datetime import datetime
import random
from faker import Faker
from faker.providers import BaseProvider
from libraries_1 import *
fake = Faker()
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# Create a Chrome webdriver
driver = webdriver.Chrome(options = chrome_options)
wait = WebDriverWait(driver, 10)



input_file = 'master_json_file.json'
output_file = 'dropdown_selection.json'
application_type = 1
filled_inputs=set()
clicked_buttons=set()
expanded_list=set()



# json_generator(input_file,output_file)

# json loader called in to load json files
json_data_1 = json_loader('feild_values.json')
dropdown_selection_json = json_loader('dropdown_selection.json')
peril_list_json = json_loader('peril_list.json')


def json_generator(input_file, output_file):
       state_code_random_choice =""
       with open(input_file, 'r') as f:
        data = json.load(f)
        random_data = {}
        for key, value in data.items():
            if isinstance(value, list) and value:
                choice = random.choice(value)
                # random_data[key] = choice
                if "state" in key and not state_code_random_choice:
                    state_code_random_choice = choice
                    random_data[key] = state_code_random_choice
                elif "state" in key and state_code_random_choice:
                    random_data[key] = state_code_random_choice
                else:
                    random_data[key] = choice
                    pass
            else:
                random_data[key] = value
        
        with open(output_file, 'w') as f:
            json.dump(random_data, f, indent=4)

login_url = "https://sandbox.socotra.com/login"

login_to_socotra(driver,login_url)

temp_url = 'https://sandbox.socotra.com/policy/100023566/quotes/100023572/exposures/100023614'

driver.get(temp_url)

vehicle_check_xpath ="//p[text()='Vehicle']"
# WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"////p[text()='Vehicle']')]")))

list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_inputs(driver,wait,vehicle_check_xpath,json_data_1,dropdown_selection_json,filled_inputs)

wait.until(is_page_loaded)

list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_inputs(driver,wait,vehicle_check_xpath,json_data_1,dropdown_selection_json,filled_inputs)