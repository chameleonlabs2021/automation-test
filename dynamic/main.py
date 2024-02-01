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

def is_scroll_complete(driver):
    return driver.execute_script("return (window.innerHeight + window.scrollY) >= document.body.scrollHeight;")

def scroll_to_location(type,element):
    print(element)    
    print(type)
    if type == 'ID':
      print('testing')              
      scroll_location = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element)))
    elif type =='XPATH':
      scroll_location = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, element)))
    driver.execute_script('arguments[0].scrollIntoView(true)',scroll_location)
    wait.until(is_scroll_complete)
    

driver.get(policy_holder_url)

# waiting for overview page to load
wait.until(is_page_loaded)

#product selector
application_type_selector(driver,1)

# wait.until(is_page_loaded)

#search all inputs and feild all dropdowns menus randomly
list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_dropdown_inputs(driver,scroll_to_location,wait)

#start and end date setter
datesetter(driver, wait)

# payment schedule selector
payment_Schedule_Selctor(driver,random.randint(1, 2))

if multiple_drivers == True:
   print("multiple_drivers is true")
   additional_driver_details(driver)






#-------- result printing -------------------------------
# print(f"total inputs found :{len(list_of_inputs)}")
# print(f"filled inputs:{failed_inputs}")