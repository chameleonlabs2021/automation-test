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
from libraries import *
fake = Faker()
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)




with open('feild_values.json', 'r') as file:
    json_data_1 = json.load(file)

with open('dropdown_selection.json', 'r') as file:
    dropdown_selection_json = json.load(file)


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
    # print(element)    
    # print(type)
    if type == 'ID':
      # print('testing')              
      scroll_location = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element)))
    elif type =='XPATH':
      scroll_location = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, element)))
    driver.execute_script('arguments[0].scrollIntoView(true)',scroll_location)
    wait.until(is_scroll_complete)

create_policyholder_button(driver)


# Wait for the page to load
time.sleep(2)

# Select the "New Policyholder" option
new_policyholder_dropdown(driver)

# driver.get(policy_holder_url)

# waiting for overview page to load
wait.until(is_page_loaded)


key_policyholder_form ='/html/body/div[1]/div[2]/div/form/div/div[3]/div/div/div/input'
# list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_inputs(driver,scroll_to_location,wait,key_policyholder_form)
list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_inputs_xpath(driver,scroll_to_location,wait,key_policyholder_form,json_data_1,dropdown_selection_json)
policyholder_create_button(driver)


# driver.get(policy_holder_url)

# waiting for overview page to load
wait.until(is_page_loaded)

#product selector
application_type_selector(driver,1)


key_policy_form ='/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[2]/div/div/div/div/div/div/input'                          
key_exposure_form ='/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/div/button'

wait.until(is_page_loaded)

#search for all button in the section and click to expand the accordion
button_finder(driver,key_policy_form)

#search all inputs and feild all dropdowns menus randomly
list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_inputs(driver,scroll_to_location,wait,key_policy_form,json_data_1,dropdown_selection_json)

#click on exposure
click_link_by_text(driver, "Exposures")
# Example usage
click_button_by_text(driver, "Add Exposure", "MuiFab-root")



wait.until(is_page_loaded)

list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_inputs_explosure(driver,scroll_to_location,wait,key_exposure_form)
#start and end date setter
# datesetter(driver, wait)

# payment schedule selector
# payment_Schedule_Selctor(driver,random.randint(1, 2))

# if multiple_drivers == True:
#    print("multiple_drivers is true")
#    additional_driver_details(driver)






#-------- result printing -------------------------------
# print(f"total inputs found :{len(list_of_inputs)}")
# print(f"filled inputs:{failed_inputs}")