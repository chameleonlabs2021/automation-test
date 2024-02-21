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

#=======================================================================

input_file = 'master_json_file.json'
output_file = 'dropdown_selection.json'
application_type = 1
filled_inputs=set()
clicked_buttons=set()
expanded_list=set()



json_generator(input_file,output_file)

# json loader called in to load json files
json_data_1 = json_loader('feild_values.json')
dropdown_selection_json = json_loader('dropdown_selection.json')
peril_list_json = json_loader('peril_list.json')
#== application type: Auto Insurance:1 ,Jewel protect:2, protect:3, Deposit Dynamic :4,Depost fixed :5, Vehicle:6 =======

#===================================== form xpath address start ====================================================================

key_policy_form ="//div[starts-with(@class,'BodyContainer')]"                         
# # # key_exposure_form ='/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/div/button'
key_create_policy_holder_form = "//form[contains(@class,'MuiBox-root css-0')]"

#===================================== form xpath address ends =====================================================================


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
login_to_socotra(driver,login_url)

# driver.get(policy_holder_url)

# # create_policyholder_button(driver)

# # Wait for the page to load
wait.until(is_page_loaded)
# # time.sleep(2)

create_new(driver, 2)
# # Select the "New Policyholder" option
# # new_policyholder_dropdown(driver)


# # # # #search all inputs and feild all dropdowns menus randomly
list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_inputs(driver,wait,key_create_policy_holder_form,json_data_1,dropdown_selection_json,filled_inputs)

wait.until(is_page_loaded)
#create button after filling the policy holder form
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//form/div/div[20]/div/button[2]"))).click()

# driver.get(policy_holder_url)
# driver.get("https://sandbox.socotra.com/policy/100017896/quotes/100017902/details")
circular_loader_wait(driver)

# WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//span[starts-with(@class,'MuiCircularProgress')]")))
# print('test1')
# WebDriverWait(driver,10).until(EC.invisibility_of_element_located((By.XPATH,"//span[starts-with(@class,'MuiCircularProgress')]")))
# print('test2')
# //span[starts-with(@class,'MuiCircularProgress')]

wait.until(is_page_loaded)
# #product selector
application_type_selector(driver,application_type)


wait.until(is_page_loaded)

button_finder(driver,clicked_buttons)

accordian_expanded(driver,expanded_list)

list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_inputs(driver,wait,key_policy_form,json_data_1,dropdown_selection_json,filled_inputs)

button_finder(driver,clicked_buttons)

accordian_expanded(driver,expanded_list)

list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_inputs(driver,wait,key_policy_form,json_data_1,dropdown_selection_json,filled_inputs)

scroll_back_to = "//div[starts-with(@class,'BodyContainer')]/div"
scroll_to_location(driver,'XPATH',scroll_back_to,wait )
# # # payment schedule selector
payment_Schedule_Selctor(driver,random.randint(1, 2))


Add_exposure(driver,application_type)

wait.until(is_page_loaded)

vehicle_check_xpath ="//p[text()='Vehicle']"
# WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"////p[text()='Vehicle']')]")))

list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_inputs(driver,wait,vehicle_check_xpath,json_data_1,dropdown_selection_json,filled_inputs)

wait.until(is_page_loaded)

list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_inputs(driver,wait,vehicle_check_xpath,json_data_1,dropdown_selection_json,filled_inputs)
#parameters for Add exposure: driver,application_type,sidebar_link_selection,exposure_dropdown_selection
# for i in range(5):
#     Add_exposure(driver,2,1,i+1)

policy_logger(driver)

#button click to lock and price or save or to select other options
top_container_button_options(driver,2)


# # waiting for overview page to load
# wait.until(is_page_loaded)

# #product selector
# application_type_selector(driver,2)


# wait.until(is_page_loaded)


# # # #search for all button in the section and click to expand the accordion
# button_finder(driver,clicked_buttons)

# accordian_expanded(driver,expanded_list)

# # # # #search all inputs and feild all dropdowns menus randomly
# list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_inputs(driver,wait,key_create_policy_holder_form,json_data_1,dropdown_selection_json,filled_inputs)


# driver.find_element(By.XPATH,"//form[contains(@class,'MuiBox-root css-0')]/div/child::*[last()]/div/button[2]").click()


# # #product selector
# application_type_selector(driver,application_type)

# wait.until(is_page_loaded)

# button_finder(driver,clicked_buttons)

# accordian_expanded(driver,expanded_list)

# list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_inputs(driver,wait,key_policy_form,json_data_1,dropdown_selection_json,filled_inputs)

# button_finder(driver,clicked_buttons)

# accordian_expanded(driver,expanded_list)

# list_of_inputs, failed_inputs, multiple_drivers = search_and_fill_all_inputs(driver,wait,key_policy_form,json_data_1,dropdown_selection_json,filled_inputs)
# # # # payment schedule selector
# payment_Schedule_Selctor(driver,random.randint(1, 2))

#================================ test ends
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



# # if multiple_drivers == True:
# #    print("multiple_drivers is true")
# #    additional_driver_details(driver)

# #-------- result printing -------------------------------
# # print(f"total inputs found :{len(list_of_inputs)}")
# # print(f"filled inputs:{failed_inputs}")


#============================= login>>application select>> fill application=========================


#============================ peril test start =============================================
# login_to_socotra(driver,test_url)

# driver.get(test_url_peril2)

# # click_link_by_text(driver, 'Exposures')
# peril_matcher(driver,peril_list_json)

# # perils_fetched_from_webpage = peril_fetcher(driver)
# # print(perils_fetched_from_webpage)

# # # add_list = missing_peril(driver,perils_fetched_from_webpage,peril_list_json)
# # # # perils_matcher(driver,perils_fetched_from_webpage,peril_list_json) 

# add_list= ["Bodily Injury","Road Side Service","Comprehensive - Actual Cash Value"]

# times = 3
# for item in add_list:    
#     add_peril_to_webpage(driver,item,times)
#     times = times+1
#============================== peril test end =======================================================