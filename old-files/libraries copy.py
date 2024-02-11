import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import random
from faker import Faker
from faker.providers import BaseProvider
fake = Faker()





#obsolete function
def _search_and_fill_all_dropdown_inputs(driver,scroll_to_location,wait,):
    create_menu_loading_check = WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.ID,'policyStart')))
    inputlist = driver.find_elements(By.TAG_NAME, 'input')
    listofitems = {}
    failed_inputs = 0
    multiple_drivers = False
    for input_element in inputlist:
        key = input_element.get_attribute("id")
        value = input_element.get_attribute("aria-autocomplete")
        field_type = input_element.get_attribute("type")
        listofitems[key] = value
        try:
            dummycheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,key)))
            driver.find_element(By.ID,key).click()
            if value == 'list':
                link1 = (f"//ul[contains(@id,'{key}-listbox')]")
                ul_element = driver.find_element(By.XPATH,link1)
                # dummycheck2 = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,ul_element )))
                li_elements = ul_element.find_elements(By.TAG_NAME,"li")
                selected_li = random.choice(li_elements)
            else:
                input_feild_fill(driver.find_element(By.ID, key))
                # driver.find_element(By.ID, key).send_keys(fake)

            if key == "policyForm.multiple_drivers" and int(selected_li.get_attribute("data-option-index"))== 1:
                multiple_drivers = True
                # print("multiple driver selected")
            selected_li.click()
        except:
            failed_inputs += 1
            # print(key)
            pass
    items_filled = len(listofitems)- failed_inputs
    # print(multiple_drivers)
    newelement = 'policy_id'
    
    scroll_to_location('ID',newelement)
    return listofitems, items_filled ,multiple_drivers

def search_and_fill_all_inputs(driver,scroll_to_location,wait,key_policy_form,json_data_1,dropdown_selection_json):
    create_menu_loading_check = WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.XPATH,key_policy_form)))
    inputlist = driver.find_elements(By.TAG_NAME, 'input')
    listofitems = {}
    failed_inputs = 0
    multiple_drivers = False
    for input_element in inputlist:
        key = input_element.get_attribute("id")
        value = input_element.get_attribute("aria-autocomplete")
        field_type = input_element.get_attribute("type")
        selection = input_element.get_attribute("value")
        listofitems[key] = value
        # print(f"{key} : {value}")
        avoid_list =['react-select-4-input','mui-9','react-select-5-input']
        if key in avoid_list:
            print(f"{key} dropdown found in ignorelist")
        else:            
            try:
                dummycheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,key)))
                if value == 'list':
                    print('==========>here<=========')
                    # dropdown_selector_random(driver,key)
                    dropdown_selector_json(driver,key,dropdown_selection_json)
                elif field_type == 'tel':
                    driver.find_element(By.ID,key).click()
                    datesetter_generic(driver,wait,key)
                else:
                    driver.find_element(By.ID,key).click()
                    feild_filler(driver,key,field_type,json_data_1)
            except:
                failed_inputs += 1
                # print(key)
                pass

    items_filled = len(listofitems)- failed_inputs
    # print(multiple_drivers)
    newelement = 'policy_id'
    scroll_to_location('ID',newelement)
    return listofitems, items_filled ,multiple_drivers

def payment_Schedule_Selctor(driver,selection):
    try:
        driver.find_element(By.ID, "payment-schedule-selector").click()
        # print("payment selector clicked")
    except:
        print("payment Schedule dropdown not found!")

    try:
        dropdownchecker = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID, 'react-select-5-option-0')))
        testoption1 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[4]/div/div/div[2]/div/div/div[1]').text
        testoption2 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[4]/div/div/div[2]/div/div/div[2]').text
        # if testoption1 == "Up Front" and testoption2 =="Monthly":
        link = (f'/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[4]/div/div/div[2]/div/div/div[{selection}]')
        driver.find_element(By.XPATH, link).click()
        # print('payment schedule selection sucessfull')
    except:
        print("payment Schedule dropdown dropdown options cant be located")

def additional_driver_details(driver,driverlicensestate= 3,designation= 2):
    try:
        buttoncheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[8]/div/div/div[1]/button')))
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[8]/div/div/div[1]/button').click()
    except:
        print("add new button not found")
    try:
        accordioncheck= WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[8]/div/div/div[2]/div/div/div[1]')))
        driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[8]/div/div/div[2]/div/div/div[1]").click()
        # print("aditional driver details accordion clicked")
    except:
        print("aditional driver details accordion  not found!")
    
    try:
        formcheck1= WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[8]/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div[1]/div/div/div/input')))
        formcheck2= WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID, 'policyForm.drivers.0.driver_lastname')))
        formcheck3= WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID, 'policyForm.drivers.0.driver_license')))
        time.sleep(1)

        driver.find_element(By.ID,"policyForm.drivers.0.driver_firstname").send_keys(fake.first_name())
        driver.find_element(By.ID,"policyForm.drivers.0.driver_lastname").send_keys(fake.last_name())
        driver.find_element(By.ID,"policyForm.drivers.0.driver_license").send_keys(random.randint(100000000, 999999999))
        #0-49
        statecheck =WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,'policyForm.drivers.0.driver_license_state')))
        driver.find_element(By.ID,'policyForm.drivers.0.driver_license_state').click()
        statechecklist =WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,'policyForm.drivers.0.driver_license_state-option-48')))
        link1 = (f'/html/body/div[5]/div/ul/li[{random.randint(1, 49)}]')
        driver.find_element(By.XPATH, link1).click()
        designationcheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,'policyForm.drivers.0.driver_designation')))
        driver.find_element(By.ID,'policyForm.drivers.0.driver_designation').click()
        designationlist =WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,'policyForm.drivers.0.driver_designation-option-5')))
        link2 = (f'policyForm.drivers.0.driver_designation-option-{random.randint(0, 5)}')
        driver.find_element(By.ID, link2).click()

    except:
        print('error22')

#obselete function
def datesetter(driver, wait):
      startdate = fake.date_between(start_date='today', end_date='+3y')
      enddate = fake.date_between(start_date='+3y', end_date='+30y')
    #   element_to_scroll_back = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located(By.XPATH, "/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[2]/div/div/div/div/div/div/input"))
    #   driver.execute_script("arguments[0].scrollIntoView();", element_to_scroll_back)
      #policy start date
      try:
        dummycheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,"policyStart")))
        driver.find_element(By.ID,"policyStart").click()
        driver.find_element(By.ID,"policyStart").send_keys(Keys.CONTROL, 'a')
        driver.find_element(By.ID,"policyStart").send_keys(Keys.DELETE)
        driver.find_element(By.ID,"policyStart").send_keys(startdate.strftime('%Y/%m/%d'))
        driver.find_element(By.ID,"policyStart").send_keys(Keys.RETURN)
        # policy end date
        driver.find_element(By.ID,"policyEnd").click()
        driver.find_element(By.ID,"policyEnd").send_keys(Keys.CONTROL, 'a')
        driver.find_element(By.ID,"policyEnd").send_keys(Keys.DELETE)
        driver.find_element(By.ID,"policyEnd").send_keys(enddate.strftime('%Y/%m/%d'))
        driver.find_element(By.ID,"policyEnd").send_keys(Keys.RETURN)
      except:
        print()

# generic datesetter
def datesetter_generic(driver, wait,key):
    # print("====>",key)
    if key == 'policyStart' or key== 'policyEnd':
        startdate = fake.date_between(start_date='today', end_date='+3y')
        enddate = fake.date_between(start_date='+3y', end_date='+30y')
        try:
            dummycheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,"policyStart")))
            driver.find_element(By.ID,"policyStart").click()
            driver.find_element(By.ID,"policyStart").send_keys(Keys.CONTROL, 'a')
            driver.find_element(By.ID,"policyStart").send_keys(Keys.DELETE)
            driver.find_element(By.ID,"policyStart").send_keys(startdate.strftime('%Y/%m/%d'))
            driver.find_element(By.ID,"policyStart").send_keys(Keys.RETURN)
            # policy end date
            driver.find_element(By.ID,"policyEnd").click()
            driver.find_element(By.ID,"policyEnd").send_keys(Keys.CONTROL, 'a')
            driver.find_element(By.ID,"policyEnd").send_keys(Keys.DELETE)
            driver.find_element(By.ID,"policyEnd").send_keys(enddate.strftime('%Y/%m/%d'))
            driver.find_element(By.ID,"policyEnd").send_keys(Keys.RETURN)
        except:
            print('Policy start or end loaded')
    else:
        try:
            dummycheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,key)))
            placeholder = driver.find_element(By.ID,key).get_attribute("placeholder")
            # print(placeholder)
            strptime_format = placeholder.replace('yyyy', '%Y').replace('mm', '%m').replace('dd', '%d').replace('hh','%I').replace('mm','%M').replace('ss','%S').replace('(am|pm)', '%#p')
            # print(strptime_format)
            label = driver.find_element(By.XPATH,f"//label[@for='{key}']")
            suitable_date = date_to_label_matcher(label.text)
            # print('=========<',suitable_date)
            # print('=========>',suitable_date.strftime(strptime_format))
            driver.find_element(By.ID,key).click()
            driver.find_element(By.ID,key).send_keys(Keys.CONTROL, 'a')
            driver.find_element(By.ID,key).send_keys(Keys.DELETE)
            driver.find_element(By.ID,key).send_keys(suitable_date.strftime(strptime_format))
            driver.find_element(By.ID,key).send_keys(Keys.RETURN)
        except:
            print()

def application_type_selector(driver,product = 1):   
    try:
      #to make sure the form is loaded by checking if first name feild is loaded 
      dummycheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/div[1]/div[2]/main/div/div[1]/div/a")))
      startbutton = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/main/div/div[1]/div/a")
      startbutton.click()
    except:
      print("Url not loaded")
      driver.quit() 

    try:
      #checking if  new application form is loaded
      startApplication_check = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/div[1]/div[2]/div/div/div[1]/div/div")))
      #dropdown menu element selection and click
      dropdown1 = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div/div")
      dropdown1.click()
      #checking if the dropdown is activated
      dummycheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/div[4]/div[3]/ul/li[1]")))
      # product Auto Insurance selected
      link = (f'/html/body/div[4]/div[3]/ul/li[{product}]')
      driver.find_element(By.XPATH, link).click()
      #select and click the create button
      driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div[3]/button[2]").click()
    except:
      print("application dropdown selection and submission failed")
      driver.quit() 

def check_required_feilds(field_element):    
    if "required" in field_element.get_attribute("outerHTML"):
        print("required element located")
        print(field_element.get_attribute("id"))
    else:
        print("non-required element located")
        print(field_element.get_attribute("id"))

    # try:
    #   dummycheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID, "payment-schedule-selector")))
    #   #  dummycheck2 = driver.find_element(By.ID, "payment-schedule-selector")
    # except:
    #     driver.quit()

def input_feild_fill(field_element):
    check_required_feilds(field_element)

#Obsolete function
def _dropdown_selector(driver,key):
    try:
        link1 = (f"//ul[contains(@id,'{key}-listbox')]")
        ul_element = driver.find_element(By.XPATH,link1)
        # dummycheck2 = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,ul_element )))
        li_elements = ul_element.find_elements(By.TAG_NAME,"li")
        # print(li_elements)
        selected_li = random.choice(li_elements)
        # print(selected_li)
        time.sleep(.25)
        selected_li.click() 
        time.sleep(.25)
        # print(f"dropdown success {key} ")  
    except:
        print(f"Dropdown {key} selection failed")

def dropdown_selector_random(driver,key):
    avoid_list =['react-select-4-input','mui-9','react-select-5-input']
    if key in avoid_list:
        print(f"{key} dropdown ignored")        
    else:
        selection = driver.find_element(By.ID,key).get_attribute("value")
        # print(selection)
        dropdown_element =driver.find_element(By.ID,key)
        dropdown_element.find_element(By.XPATH, "following-sibling::*").click()
        count = 0
        while not selection:          
            try:
                link1 = (f"//ul[contains(@id,'{key}-listbox')]")
                ul_element = driver.find_element(By.XPATH,link1)
                # dummycheck2 = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,ul_element )))
                li_elements = ul_element.find_elements(By.TAG_NAME,"li")
                # print(type(li_elements))
                new_li_elements = []
                for item in li_elements:
                    content = item.get_attribute("innerText")
                    # print(content)
                    if content == 'none' or content == 'None':
                        pass
                    else:
                        new_li_elements.append(item)
                # print(new_li_elements)
                selected_li = random.choice(new_li_elements)
                # print(selected_li)
                selected_li.click() 
                selection = driver.find_element(By.ID,key).get_attribute("value")
            except:
                print(f"Dropdown {key} selection failed")

def dropdown_selector_json(driver,key,dropdown_selection_json):
    avoid_list =['react-select-4-input','mui-9','react-select-5-input']
    if key in avoid_list:
        print(f"{key} dropdown ignored")        
    else:
        for json_key, value in dropdown_selection_json.items():
            # json_key_new = json_key.lower()
            print(key,'<========>',json_key)
            if json_key  in key:            
                selection = driver.find_element(By.ID,key).get_attribute("value")
                # print(selection)
                dropdown_element =driver.find_element(By.ID,key)
                dropdown_element.find_element(By.XPATH, "following-sibling::*").click()
                count = 0
                while not selection:
                    if count > 10:
                        break          
                    try:
                        
                        link1 = (f"//ul[contains(@id,'{key}-listbox')]")
                        ul_element = driver.find_element(By.XPATH,link1)
                        # dummycheck2 = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,ul_element )))
                        li_elements = ul_element.find_elements(By.TAG_NAME,"li")
                        # print(type(li_elements))
                        for item in li_elements:
                            content = item.get_attribute("innerText")
                            # print(content)
                            value = value.lower()
                            content = content.lower()
                            if value == content:
                                selected_li = item
                                break
                            else:
                                pass
                        # print(selected_li)
                        selected_li.click() 
                        selection = driver.find_element(By.ID,key).get_attribute("value")
                    except:
                        count+=1
                        print(f"Dropdown {key} selection failed")
            else:
             print(f"{key} dropdown selection data missing in json file")
  
def feild_filler(driver,key,field_type,json_data_1):
    # print(key)
    try:
        if field_type == 'text':
            # input_feild = driver.find_element(By.ID,key)
            # input_feild.send_keys(fake.sentence())
            # print(f"text feild success {key} ")
            fake_data_based_on_id(driver,key,json_data_1)  
        elif field_type == "number":
            input_field = driver.find_element(By.ID,key)
            input_field.send_keys(fake.random_int(min=1, max=100))
            # print(f"number field success {key} ")  
        elif field_type == "email":
            input_field = driver.find_element(By.ID,key)
            input_field.send_keys(fake.email())
            # print(f"email field success {key} ")  
        # elif field_type == "tel":
        #     random_date = fake.date_time()
        #     input_feild = driver.find_element(By.ID,key)
        #     place_holder = input_feild.get_attribute("placeholder")
        #     print(place_holder)
        #     input_feild.send_keys(random_date.strftime("%Y/%m/%d %I:%M:%S %p"))
        #     print(f"number feild success {key} ")  
      
    except:
        print(f"Dropdown {key} selection failed")
    
def date_to_label_matcher(label):
    if label == 'calendar date entry':
        return datetime.today().date()
    
    if label == 'Year of Make *':
        date_new= fake.date_between(start_date='today', end_date='-10y')
        return date_new
    else:
        return fake.date_time_this_decade()
        
def button_finder(driver,key):
    create_menu_loading_check = WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.XPATH,key)))
    section_elements = driver.find_elements(By.TAG_NAME, 'section')
    for section in section_elements:
        buttonlist = section.find_elements(By.TAG_NAME, 'button')
        # listofitems = {}
        # failed_inputs = 0
        # multiple_drivers = False
        for button in buttonlist: 
            # key = button.get_attribute("id")
            text = button.get_attribute("innerHTML")
            field_type = button.get_attribute("type")
            #checking if button is a dropdown arrowicon
            button_aria_label = button.get_attribute("aria-label")
            # print(text,'===', field_type)
            try:
                label = button.find_element(By.XPATH, "preceding-sibling::label")
                # print(label.text)
                parent_element = label.find_element(By.XPATH, "..")
                following_sibling = parent_element.find_element(By.XPATH, "following-sibling::*")
                button.click()
                time.sleep(.3)               
                # following_sibling = parent_element.find_element(By.XPATH, "following-sibling::*")
                following_sibling.click()
                # print('testing')
            except:
                if button_aria_label == 'Close' or button_aria_label  == 'Open':
                    print("Dropdown arrow icon Button ignorned")
                else:
                    print(f"button selection and accordin click failed")

def accordian_expanded():
    pass

def fake_data_based_on_id(driver,key,json_data_1):
    fake = Faker('en_US') 
    
    for json_key, value in json_data_1.items():

        json_key_new = json_key.lower()
        if json_key_new  in key:       
            # print(f"======>{key} : {json_key_new}<=========")     
            fake_data = eval(f"{value}")
            # print(fake_data)
            input_field = driver.find_element(By.ID,key)
            input_field.send_keys(fake_data)
            # print("test json")
            # print(value)
        # if json_key_new.find(key) != -1:
        #     print("test passed")
        else:
             print(f"{key} input data push failed:'fake_data_based_on_id'")

#===================== field data filling functions below ======================#

def iso_territory_code():
    return 'US'

def iso_protection_class():
    list_iso =["ISO-1", "ISO-2", "ISO-3", "ISO-4", "ISO-5", "ISO-6", "ISO-7", "ISO-8", "ISO-9"]
    choice = random.choice(list_iso)
    return choice

def rater_ID():
    list_rater_ID =["RX6846", "MA3694", "YX6984", "HS9734"]
    choice = random.choice(list_rater_ID)
    return choice






if __name__ =="__main__":
    print("...")