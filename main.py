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

#== application type: Auto Insurance:1 ,Jewel protect:2, protect:3, Deposit Dynamic :4,Depost fixed :5, Vehicle:6 =======
# options 1,2,3,4,5,6 Application type selection
application_type = 2
# min [1] max [1,2,3,4,5] covers all five exposures
exposure_selection =[1,2,3]

#variables to track all ready filled in fields
filled_inputs=set()
clicked_buttons=set()
expanded_list=set()


#========================= json related files start==========================================

#this function creates a dropdown_selection_json on the fly using the master_json_file
json_generator(input_file,output_file)
# json loader called in to load json files
field_value_json = json_loader('field_values.json')
dropdown_selection_json = json_loader('dropdown_selection.json')
peril_list_json = json_loader('peril_list.json')

#========================= json related files end=============================================

#===================================== form xpath address start ====================================================================

key_policy_form ="//div[starts-with(@class,'BodyContainer')]"                         
# # # key_exposure_form ='/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/div/button'
policy_holder_form_locator = "//form[contains(@class,'MuiBox-root css-0')]"

#===================================== form xpath address end =====================================================================


#================ test variable start ======================================
#test url for peril
test_url = 'https://sandbox.socotra.com/policy/100000656/quotes/100000662/exposures/100013506'
person1 = "7e22ad18-4382-4455-8022-2ea631872f8c"
test_url_peril = f"https://sandbox.socotra.com/policyholder/{person1}"
test_url_peril2 = 'https://sandbox.socotra.com/policy/100000656/quotes/100000662/exposures/100013506/perils'

# 522855ef-1536-410b-b4a6-a425f7c03723
policy_holder_url = f"https://sandbox.socotra.com/policyholder/{person1}"

login_url = "https://sandbox.socotra.com/login"

#================ test variable end ======================================
#====================params ==============================================

params = {"driver": driver,"wait": wait, "login_url":login_url,"key_policy_form" :key_policy_form,"policy_holder_form_locator": policy_holder_form_locator,
          "field_value_json":field_value_json,"dropdown_selection_json": dropdown_selection_json, "peril_list_json": peril_list_json, "filled_inputs":filled_inputs,
            "clicked_buttons":clicked_buttons,"expanded_list":expanded_list,"application_type":application_type,"exposure_selection":exposure_selection}


#============================= login>>application select>> fill application=========================
# # #login to socotra credintial hardcoded in the function/ credintial to be move to a ENV file
# login_to_socotra(driver,login_url)

# # # Wait for the page to load
# wait.until(is_page_loaded)
# # # time.sleep(2)

# # Create a new policy holder. 
# create_new(driver,wait, 2,policy_holder_form_locator,field_value_json,dropdown_selection_json,filled_inputs)
# # # Select the "New Policyholder" option
# # # new_policyholder_dropdown(driver)

# #circular loader waiting function
# circular_loader_wait(driver)

# wait.until(is_page_loaded)

# # #product selector application type can be defined in the start of this page.
# application_type_selector(driver,application_type)

# # all the variables are passed into the sequence function through params. Params is dictionary defined in the start of this page.
# application_type_1(params)

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
if __name__ =="__main__":        
    # #login to socotra credintial hardcoded in the function/ credintial to be move to a ENV file
    login_to_socotra(driver,login_url)

    # # Wait for the page to load
    wait.until(is_page_loaded)
    # # time.sleep(2)

    # Create a new policy holder. 
    create_new(driver,wait, 2,policy_holder_form_locator,field_value_json,dropdown_selection_json,filled_inputs)
    # # Select the "New Policyholder" option
    # # new_policyholder_dropdown(driver)

    #circular loader waiting function
    circular_loader_wait(driver)

    wait.until(is_page_loaded)

    # #product selector application type can be defined in the start of this page.
    application_type_selector(driver,application_type)

    # all the variables are passed into the sequence function through params. Params is dictionary defined in the start of this page.
    application_type_1(params)


