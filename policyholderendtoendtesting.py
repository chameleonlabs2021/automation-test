import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from faker import Faker

import time
import random
from libraries import *
fake = Faker()
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options = chrome_options)
wait = WebDriverWait(driver, 10)

login_to_socotra(driver)

# Wait for the page to load
time.sleep(2)

create_policyholder_button(driver)


# Wait for the page to load
time.sleep(2)

# Select the "New Policyholder" option
new_policyholder_dropdown(driver)

# driver.get(policy_holder_url)

# waiting for overview page to load
wait.until(is_page_loaded)

#Read data from csv and fill all fields
all_fields_successful=load_config( driver,'policyholder.csv')



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

# Click the "Create" button if all fields were successfully filled
if all_fields_successful:
    policyholder_create_button(driver)
    time.sleep(2)
    print("Policyholder created successfully")

# waiting for overview page to load
wait.until(is_page_loaded)

#product selector
application_type_selector(driver,1)

wait.until(is_page_loaded)


#search all inputs and feild all dropdowns menus randomly
list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_dropdown_inputs(driver,scroll_to_location,wait,'//*[@id="policyStart"]')

#start and end date setter
# datesetter(driver, wait)

# payment schedule selector
# payment_Schedule_Selctor(driver,random.randint(1, 2))

# if multiple_drivers == True:
#    print("multiple_drivers is true")
#    additional_driver_details(driver)


#click on exposure
click_link_by_text(driver, "Exposures")
# Example usage
click_button_by_text(driver, "Add Exposure", "MuiFab-root")


wait.until(is_page_loaded)
#search all inputs and feild all dropdowns menus randomly
list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_dropdown_inputs(driver,scroll_to_location,wait,'/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/div/button')

#-------- result printing -------------------------------
print(f"total inputs found :{len(list_of_inputs)}")
print(f"filled inputs:{failed_inputs}")