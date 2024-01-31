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
from faker import Faker
from libraries import *
fake = Faker()
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Replace with the actual JSON data
json_data = '''{
  "pages": [
    {
      "sections": [
        {
          "title": "Primary Policyholder",
          "fields": [
            {
              "name": "first_name",
              "prompt": "First Name",
              "required": true,
              "updateable": true,
              "width": 4
            },
            {
              "name": "last_name",
              "prompt": "Last Name",
              "required": true,
              "updateable": true,
              "width": 4
            },
            {
              "name": "email",
              "prompt": "Email",
              "required": false,
              "updateable": true,
              "width": 4
            },
            {
              "name": "phone_number",
              "prompt": "Phone number",
              "required": false,
              "updateable": true,
              "width": 4
            }
          ]
        }
      ]
    }
  ]
}'''

# Parse the JSON data
data = json.loads(json_data)

# Create a Chrome webdriver
driver = webdriver.Chrome(options = chrome_options)
wait = WebDriverWait(driver, 10)
# Replace with the actual URL to login
login_url = "https://sandbox.socotra.com/login"
driver.get(login_url)
person1 = "7e22ad18-4382-4455-8022-2ea631872f8c"
# 522855ef-1536-410b-b4a6-a425f7c03723
policy_holder_url = f"https://sandbox.socotra.com/policyholder/{person1}"

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

def is_page_loaded(driver):
    return driver.execute_script("return document.readyState === 'complete';")

def page_scrolled_to_top(driver):
    return driver.execute_script("return window.scrollY === 0;")

# Wait for the page to load
time.sleep(2)

create_policyholder_button(driver)


# Wait for the page to load
time.sleep(2)

new_policyholder_dropdown(driver)

# driver.get(policy_holder_url)

# waiting for overview page to load
wait.until(is_page_loaded)

csv_file_path = 'policyholder.csv'
data_list = read_data_from_csv(csv_file_path)

# Define the regex pattern
regex_pattern = "policyholder\.tenant_[a-z0-9]+_{}"

# Iterate through the list of data and fill in the fields
all_fields_successful = True
for item in data_list:
    title = item['title']
    data_to_input = item['data']
    field_type = item['type']
    specific_pattern = regex_pattern.format(re.escape(title))

    if field_type == 'select':
        # success = handle_custom_dropdown(driver, title, data_to_input, specific_pattern)
        # success= find_element_with_dynamic_id(driver, specific_pattern)
        # Usage
        base_id = "policyholder.tenant_"
        dynamic_part = ""  # You can specify a known part of the dynamic section if applicable
        end_id = "_ofac_outcome"
        success = click_and_select_by_id_ending_with(driver, end_id, data_to_input)
        print(f"Found element: {success}")
    elif field_type == 'date': #TODO fix the date field issue
        # Handle date field
        # success = set_date_field(driver, title, specific_pattern, data_to_input)
        print(f"Setting date field {title} with value: {data_to_input} using pattern: {specific_pattern}")
    else:
        # Handle other input types
        success = handle_input_or_select(driver, title, data_to_input, specific_pattern)

    if success:
        print(f"Interaction successful for field with title: {title}")
    else:
        print(f"Failed to interact with field with title: {title}")
        all_fields_successful = False
        break  # Exit the loop if a field interaction fails

# Click the "Create" button if all fields were successfully filled
if all_fields_successful:
    policyholder_create_button(driver)
    time.sleep(2)
    print("Policyholder created successfully")



#product selector
application_type_selector(driver,1)



print("driver" , driver)
#search all inputs and field all dropdowns menus randomly
list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_dropdown_inputs(driver)

#start and end date setter
# datesetter(driver, wait,page_scrolled_to_top) #TODO fix the issue

# payment schedule selector
payment_Schedule_Selctor(driver,random.randint(1, 2))

if multiple_drivers == True:
   print("multiple_drivers is true")
   additional_driver_details(driver)


#click on exposure
click_link_by_text(driver, "Exposures")
# Example usage
click_button_by_text(driver, "Add Exposure", "MuiFab-root")


#-------- result printing -------------------------------
print(f"total inputs found :{len(list_of_inputs)}")
print(f"filled inputs:{failed_inputs}")