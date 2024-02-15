
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
import random

from libraries_1 import *

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options = chrome_options)
wait = WebDriverWait(driver, 10)
# Replace with the actual URL to login
login_url = "https://sandbox.socotra.com/login"
driver.get(login_url)

exposure_url = f"https://sandbox.socotra.com/policy/100005326/quotes/100005332/exposures/100005242"
# https://sandbox.socotra.com/policyholder/7e22ad18-4382-4455-8022-2ea631872f8c/overview
# Fill in the login details
driver.find_element(By.ID,"LoginForm__UsernameField--Standard").send_keys("alice.lee") 
driver.find_element(By.ID,"LoginForm__PasswordField--Standard").send_keys("socotra") 
driver.find_element(By.ID,"LoginForm__HostnameField--Standard").send_keys("rpoolanchalil-synpulse-configeditor.co.sandbox.socotra.com") 
driver.find_element(By.ID, "LoginForm__Button--StandardLogin").click()
# time.sleep(2) 
# time.sleep(15) 

#login page loaded check
try:
   create_menu_loading_check = WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.ID,'AppBar__Buttons--CreateDropdown')))
except:
    print("login failed or page not loaded properly")



driver.get(exposure_url)


#search all inputs and feild all dropdowns menus randomly
list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_dropdown_inputs(driver,scroll_to_location,wait)

# csv_file_path = 'vehicle_fields.csv'
# data_list = read_data_from_csv(csv_file_path)
# print(data_list)
# # Define the regex pattern
# regex_pattern = "[a-z0-9]+.{}"

# # Iterate through the list of data and fill in the fields

# all_fields_successful = True
# for item in data_list:
#     # Check the value of the 'switch' field directly
#     if item.get('switch', 'Yes') != 'No':   # Proceed only if the switch is 'Yes'
#         title = item['title']
#         data_to_input = item['data']
#         field_type = item['type']
#         specific_pattern = regex_pattern.format(re.escape(title))

#         if field_type == 'select':
#             success = vehicle_click_and_select_by_id_ending_with(driver, title, data_to_input)
#             print(f"Found element: {success}")
#         elif field_type == 'date':
#             # Handle date field
#             success = set_date_field(driver, title, specific_pattern, data_to_input)
#             print(f"Setting date field {title} with value: {data_to_input} using pattern: {specific_pattern}")
#         else:
#             # Handle other input types
#             success = vehicle_string_field_by_id_ending_with(driver, title,data_to_input)

#         if not success:
#             print(f"Failed to interact with field with title: {title}")
#             all_fields_successful = False
#             break  # Exit the loop if a field interaction fails
#     else:
#         print(f"Skipping field with title: {title} as switch is not set to 'Yes'")
#         continue

# Click the "Create" button if all fields were successfully filled
# if all_fields_successful:
#     policyholder_create_button(driver)
#     time.sleep(2)
#     print("Policyholder created successfully")

