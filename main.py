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



# json loader called in to load json files
json_data_1 = json_loader('feild_values.json')
dropdown_selection_json = json_loader('dropdown_selection.json')
peril_list_json = json_loader('peril_list.json')

#================ test variable start ======================================
#test url for peril
test_url = 'https://sandbox.socotra.com/policy/100000656/quotes/100000662/exposures/100013506'
person1 = "7e22ad18-4382-4455-8022-2ea631872f8c"
test_url_peril = f"https://sandbox.socotra.com/policyholder/{person1}"
test_url_peril2 = 'https://sandbox.socotra.com/policy/100000656/quotes/100000662/exposures/100013506/perils'

# 522855ef-1536-410b-b4a6-a425f7c03723
policy_holder_url = f"https://sandbox.socotra.com/policyholder/{person1}"

login_url = "https://sandbox.socotra.com/login"

#================ test variable finish ======================================


#============================= login>>application select>> fill application=========================
# #login to socotra credintial hardcoded in the function/ credintial to be move to a ENV file
# login_to_socotra(driver,login_url)

# driver.get(policy_holder_url)

# # create_policyholder_button(driver)

# # Wait for the page to load
# # wait.until(is_page_loaded)
# # time.sleep(2)

# # Select the "New Policyholder" option
# # new_policyholder_dropdown(driver)

# # driver.get(policy_holder_url)

# # waiting for overview page to load
# wait.until(is_page_loaded)

# #product selector
# application_type_selector(driver,3)

# filled_inputs=set()
# clicked_buttons=set()
# expanded_list=set()

# key_policy_form ='/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[2]/div/div/div/div/div/div/input'                          
# key_exposure_form ='/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/div/button'

# wait.until(is_page_loaded)

# #search for all button in the section and click to expand the accordion
# button_finder(driver,key_policy_form,clicked_buttons)

# accordian_expanded(driver,expanded_list)

# #search all inputs and feild all dropdowns menus randomly
# list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_inputs(driver,scroll_to_location,wait,key_policy_form,json_data_1,dropdown_selection_json,filled_inputs)

# button_finder(driver,key_policy_form,clicked_buttons)

# accordian_expanded(driver,expanded_list)

# list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_inputs(driver,scroll_to_location,wait,key_policy_form,json_data_1,dropdown_selection_json,filled_inputs)
# #start and end date setter
# # datesetter(driver, wait)

# # policyholder_create_button(driver)

# # driver.get(policy_holder_url)

# # waiting for overview page to load
# wait.until(is_page_loaded)


# # #click on exposure
# # click_link_by_text(driver, "Exposures")
# # # Example usage
# # click_button_by_text(driver, "Add Exposure", "MuiFab-root")

# # payment schedule selector
# # payment_Schedule_Selctor(driver,random.randint(1, 2))

# # if multiple_drivers == True:
# #    print("multiple_drivers is true")
# #    additional_driver_details(driver)

# #-------- result printing -------------------------------
# # print(f"total inputs found :{len(list_of_inputs)}")
# # print(f"filled inputs:{failed_inputs}")


#============================= login>>application select>> fill application=========================


#============================ peril test =============================================
login_to_socotra(driver,test_url)

driver.get(test_url_peril2)

# click_link_by_text(driver, 'Exposures')

peril_matcher(driver,peril_list_json)

