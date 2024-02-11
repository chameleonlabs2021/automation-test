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
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from datetime import datetime 
import time
import random
from faker import Faker
import csv
import re
from selenium.webdriver.support.ui import Select

fake = Faker()
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

def json_loader(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data

def is_page_loaded(driver):
    return driver.execute_script("return document.readyState === 'complete';")

def is_scroll_complete(driver):
    return driver.execute_script("return (window.innerHeight + window.scrollY) >= document.body.scrollHeight;")

def scroll_to_location(driver,wait,type,element):
    # print(element)    
    # print(type)
    if type == 'ID':
      # print('testing')              
      scroll_location = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element)))
    elif type =='XPATH':
      scroll_location = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, element)))
    driver.execute_script('arguments[0].scrollIntoView(true)',scroll_location)
    wait.until(is_scroll_complete)

def login_to_socotra (driver):


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
        #print("login failed or page not loaded properly")
        pass

def is_page_loaded(driver):
    return driver.execute_script("return document.readyState === 'complete';")

def page_scrolled_to_top(driver):
    return driver.execute_script("return window.scrollY === 0;")

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
    # scroll_to_location('ID',newelement)
    return listofitems, items_filled ,multiple_drivers

def search_and_fill_all_inputs_xpath(driver,scroll_to_location,wait,key_policy_form,json_data_1,dropdown_selection_json):
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
                    var1= driver.find_element(By.ID,key)
                    print(var1)
                    driver.find_element(By.ID,key).click()
                    
                    feild_filler(driver,key,field_type,json_data_1)
            except:
                failed_inputs += 1
                print("key failed")
                pass

    items_filled = len(listofitems)- failed_inputs
    # print(multiple_drivers)
    newelement = 'policy_id'
    # scroll_to_location('ID',newelement)
    return listofitems, items_filled ,multiple_drivers

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
     
def create_policyholder_button(driver):
    #print("Starting create_policyholder_button function...")
    try:
        # Find the button by ID and click it
        button = driver.find_element(By.ID, "AppBar__Buttons--CreateDropdown")
        button.click()
        #print("Clicked on create_policyholder_button.")
    except Exception as e:
        print("Error: ", e)
    finally:
        #print("Ending create_policyholder_button function...")
        pass

def click_button_by_text(driver, button_text, class_name):
    #print("Starting click_button_by_text function...")
    try:
        # Construct an XPath that matches the button based on its class and text
        button_xpath = f"//button[contains(@class, '{class_name}') and contains(., '{button_text}')]"
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        button.click()
        #print(f"Clicked on button with text '{button_text}'.")
    except TimeoutException:
        print(f"Timeout: Button with text '{button_text}' and class '{class_name}' not found or not clickable.")
    except Exception as e:
        print(f"Error while trying to click the button: {e}")
    finally:
        #print("Ending click_button_by_text function...")
        pass

def new_policyholder_dropdown(driver):
    #print("Starting new_policyholder_dropdown function...")
    try:
        # Find the button by its text and click it
        button = driver.find_element(By.XPATH, "//button[contains(.,'New Policyholder')]")
        button.click()
        #print("Clicked on new_policyholder_dropdown.")
    except Exception as e:
        print("Error: ", e)
    finally:
        #print("Ending new_policyholder_dropdown function...")
        pass

def policyholder_create_button(driver):
    #print("Starting policyholder_create_button function...")
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiButton-containedPrimary[type='submit']"))
        )
        button.click()
        #print("Clicked on policyholder_create_button.")
    except Exception as e:
        print(f"Error while trying to click the 'Create' button: {e}")
    finally:
        #print("Ending policyholder_create_button function...")
        pass

def find_element_by_regex_title(driver, title, pattern):
    #print(f"Starting find_element_by_regex_title function for title: {title}...")
    compiled_pattern = re.compile(pattern)

    try:
        input_elements = driver.find_elements(By.TAG_NAME, "input")
        for element in input_elements:
            id = element.get_attribute("id")
            if compiled_pattern.match(id):
                return element
        raise NoSuchElementException(f"No element found with title: {title}")
    except Exception as e:
        #print(f"Error while finding element: {e}")
        raise
    finally:
        #print(f"Ending find_element_by_regex_title function for title: {title}...")
        pass

def read_data_from_csv(file_path):
    #print("Starting read_data_from_csv function...")
    data_list = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data_list.append({
                'title': (row['title'] or '').strip(),
                'data': (row['data'] or '').strip(),
                'type': (row['type'] or '').strip(),
                'switch': (row['switch'] or '').strip()
            })
    #print("Ending read_data_from_csv function...")
    return data_list

def handle_custom_dropdown(driver, title, dropdown_value, pattern):
    #print(f"Starting handle_custom_dropdown function for title: {title}...")
    #print(f"Handling custom dropdown: {title} with value: {dropdown_value}")
    try:
        input_id = find_element_by_regex_title(driver, title, pattern)
        #print(f"Found element: {input_id}")
        # Click the input element to open the dropdown
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, input_id))
        )
        
        # Click the element
        element.click()
        #print(f"Clicked element: {element}")
        # Construct the XPath for the dropdown list
        dropdown_list_xpath = f"//ul[contains(@id,'{input_id}-listbox')]"
        ul_element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, dropdown_list_xpath)))

        # Find and click the correct list item
        list_items = ul_element.find_elements(By.TAG_NAME, "li")
        for item in list_items:
            if item.text == dropdown_value:
                item.click()
                #print(f"Selected value: {dropdown_value}")
                return True

        raise Exception("Dropdown value not found")
    except Exception as e:
        #print(f"Failed to interact with dropdown: {e}")
        return False
    finally:
        print(f"Ending handle_custom_dropdown function for title: {title}...")

def click_and_select_by_id_ending_with(driver, end_id, value_to_select):
    #print(f"Starting click_and_select_by_id_ending_with function for end_id: {end_id}...")
    try:
        # Construct an XPath that checks if the ID ends with end_id
        element_xpath = f"//input[substring(@id, string-length(@id) - string-length('{end_id}') + 1) = '{end_id}']"
        #print(f"Checking if element with XPath: {element_xpath} exists")
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, element_xpath))
        )
        
        # Click the element to open the dropdown or activate the component
        element.click()
        #print(f"Clicked element: {element}")

        # Assuming the value to select is visible and can be clicked
        # Adjust the selector as needed for your specific case
        # This is an example XPath and might need modification
        value_xpath = f"//li[contains(text(), '{value_to_select}')]"  # Example for a custom dropdown
        value_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, value_xpath))
        )
        value_element.click()
        #print(f"Selected value: {value_to_select}")
        return True
    except NoSuchElementException:
        #print(f"No element found with ID ending with: {end_id}")
        raise
    except TimeoutException:
        #print(f"Timeout occurred while trying to select the value: {value_to_select}")
        raise
    except Exception as e:
        #print(f"Error during click and select: {e}")
        raise
    finally:
        print(f"Ending click_and_select_by_id_ending_with function for end_id: {end_id}...")

def set_date_field(driver, title, pattern, date_value, date_format='%Y/%m/%d'):
    #print(f"Starting set_date_field for title: {title}...")
    #print(f"Setting date field {title} with value: {date_value} using pattern: {pattern}")
    element_to_scroll_back = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located(By.ID, title))
    driver.execute_script("arguments[0].scrollIntoView();", element_to_scroll_back)

    try:
        # Locate the element using the provided regex pattern
        date_field = find_element_by_regex_title(driver, title, pattern)
        #print(f"Found element: {date_field}")

        # Clear any existing value in the date field
        driver.find_element(By.ID,title).click()
        driver.find_element(By.ID,title).send_keys(Keys.CONTROL, 'a')
        driver.find_element(By.ID,title).send_keys(Keys.DELETE)
        driver.find_element(By.ID,title).send_keys(date_value.strftime('%Y/%m/%d'))
        driver.find_element(By.ID,title).send_keys(Keys.RETURN)
        # Format the date and set the new value

    except NoSuchElementException as e:
        #print(f"No such element: Could not locate element with title {title} using pattern {pattern}")
        pass
    except Exception as e:
        pass
        #print(f"Error during set_date_field for title {title}: {e}")
    finally:
        #print(f"Ending set_date_field for title: {title}...")
        pass

def is_scroll_complete(driver):
    #print("Starting is_scroll_complete...")
    result = driver.execute_script("return (window.innerHeight + window.scrollY) >= document.body.scrollHeight;")
    #print("Ending is_scroll_complete...")
    return result

# def scroll_to_location(driver, type, element):
#     #print("Starting scroll_to_location...")
#     #print(element)
#     #print(type)
    
#     try:
#         if type == 'ID':
#             #print('Testing ID')
#             scroll_location = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element)))
#         elif type == 'XPATH':
#             scroll_location = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, element)))
#         driver.execute_script('arguments[0].scrollIntoView(true)', scroll_location)
#         wait.until(is_scroll_complete)
#     except Exception as e:
#         #print(f"Error during scroll_to_location: {e}")
#         pass
#     finally:
#         #print("Ending scroll_to_location...")
#         pass

def dropdown_selector(driver,key):
    try:
        link1 = (f"//ul[contains(@id,'{key}-listbox')]")
        ul_element = driver.find_element(By.XPATH,link1)
        # dummycheck2 = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,ul_element )))
        li_elements = ul_element.find_elements(By.TAG_NAME,"li")
        # #print(li_elements)
        selected_li = random.choice(li_elements)
        # #print(selected_li)
        time.sleep(1)
        selected_li.click() 
        time.sleep(1)
        # #print(f"dropdown success {key} ")  
    except:
        #print(f"Dropdown {key} selection failed")
        pass

# Define a dictionary mapping key substrings to faker functions
key_to_faker = {
    'first_name': fake.first_name,
    'last_name': fake.last_name,
    'address': fake.address,
    'year': lambda: str(fake.year()),
    'email': fake.email,
    'id': fake.uuid4,
    'phone': fake.phone_number,
    'tel': fake.phone_number,
    'date': fake.date,
    'vin': lambda: '2HGFB2F59EH567890',  # Placeholder for dynamic VIN generation
    'zip': fake.postcode,
    'postal': fake.postcode,
    'country': fake.country,
    'city': fake.city,
    'company': fake.company,
    'title': fake.job,
    'url': fake.url,
    'description': lambda: fake.sentence(nb_words=10),
    'bio': lambda: fake.sentence(nb_words=10)
}

def generate_dummy_text(key):
    key_lower = key.lower()
    for substring, faker_func in key_to_faker.items():
        if substring in key_lower:
            return faker_func() if callable(faker_func) else faker_func
    return fake.sentence()  # Default case for unmatched keys
    
def field_filler(driver, key, field_type=None):
    key_lower = key.lower()  # Lowercase conversion for case-insensitive comparison

    try:
        # Generate text or number based on field_type or key
        if field_type in ['text', 'email', 'telephone', 'tel'] or 'year' in key_lower:
            text_to_input = generate_dummy_text(key)
            input_field = driver.find_element(By.ID, key)
            input_field.send_keys(text_to_input)
        elif field_type == 'number' or 'number' in key_lower:
            input_field = driver.find_element(By.ID, key)
            input_field.send_keys(fake.random_number(digits=5))
        else:
            print(f"No specific data type matched for {key}")
    except Exception as e:
        print(f"Field {key} filling failed: {e}")

def search_and_fill_all_inputs_explosure(driver,scroll_to_location,wait,key):
    create_menu_loading_check = WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.XPATH,key)))
    inputlist = driver.find_elements(By.TAG_NAME, 'input')
    listofitems = {}
    failed_inputs = 0
    multiple_drivers = False
    for input_element in inputlist:
        key = input_element.get_attribute("id")
        value = input_element.get_attribute("aria-autocomplete")
        field_type = input_element.get_attribute("type")
        listofitems[key] = value
        print(f"{key} : {value}")
        try:
            if key == 'mui-9':
                continue
            dummycheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,key)))
            driver.find_element(By.ID,key).click()
            if value == 'list':
                dropdown_selector(driver,key)
            elif field_type == 'tel':
                print(f"key inside tel {key}",f"value {value}",f"field_type {field_type}")
                datesetter_generic(driver,wait,key)
            else:
                print(f"elif hit")
                print(f"key {key}",f"value {value}",f"field_type {field_type}")
                field_filler(driver,key,field_type)
        except:
            failed_inputs += 1
            # print(key)
            pass

    items_filled = len(listofitems) - failed_inputs
    
    # Scroll to a new element if necessary
    newelement = 'policy_id'
    scroll_to_location('ID',newelement)


    return listofitems, items_filled, False  # Assuming multiple_drivers is not altered within this function

def payment_Schedule_Selctor(driver,selection):
    try:
        driver.find_element(By.ID, "payment-schedule-selector").click()
        #print("payment selector clicked")
    except:
        #print("payment Schedule dropdown not found!")
        pass

    try:
        dropdownchecker = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID, 'react-select-5-option-0')))
        testoption1 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[4]/div/div/div[2]/div/div/div[1]').text
        testoption2 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[4]/div/div/div[2]/div/div/div[2]').text
        # if testoption1 == "Up Front" and testoption2 =="Monthly":
        link = (f'/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[4]/div/div/div[2]/div/div/div[{selection}]')
        driver.find_element(By.XPATH, link).click()
        #print('payment schedule selection sucessfull')
    except:
        #print("payment Schedule dropdown dropdown options cant be located")
        pass

def additional_driver_details(driver, driverlicensestate=3, designation=2):
    #print("Starting additional_driver_details...")
    try:
        buttoncheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[8]/div/div/div[1]/button')))
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[8]/div/div/div[1]/button').click()
    except Exception as e:
        pass
        # #print(f"Error while clicking 'Add New' button: {e}")

    try:
        accordioncheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[8]/div/div/div[2]/div/div/div[1]')))
        driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[8]/div/div/div[2]/div/div/div[1]").click()
        #print("Additional driver details accordion clicked")
    except Exception as e:
        #print(f"Error while clicking additional driver details accordion: {e}")
        pass

    try:
        formcheck1 = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[2]/section/div/div[8]/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div[1]/div/div/div/input')))
        formcheck2 = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID, 'policyForm.drivers.0.driver_lastname')))
        formcheck3 = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID, 'policyForm.drivers.0.driver_license')))
        time.sleep(1)

        driver.find_element(By.ID,"policyForm.drivers.0.driver_firstname").send_keys(fake.first_name())
        driver.find_element(By.ID,"policyForm.drivers.0.driver_lastname").send_keys(fake.last_name())
        driver.find_element(By.ID,"policyForm.drivers.0.driver_license").send_keys(random.randint(100000000, 999999999))
        # 0-49
        statecheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,'policyForm.drivers.0.driver_license_state')))
        driver.find_element(By.ID,'policyForm.drivers.0.driver_license_state').click()
        statechecklist = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,'policyForm.drivers.0.driver_license_state-option-48')))
        link1 = (f'/html/body/div[5]/div/ul/li[{random.randint(1, 49)}]')
        driver.find_element(By.XPATH, link1).click()
        designationcheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,'policyForm.drivers.0.driver_designation')))
        driver.find_element(By.ID,'policyForm.drivers.0.driver_designation').click()
        designationlist = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,'policyForm.drivers.0.driver_designation-option-5')))
        link2 = (f'policyForm.drivers.0.driver_designation-option-{random.randint(0, 5)}')
        driver.find_element(By.ID, link2).click()

    except:
        print('error22')

#obselete
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
        
        # Policy end date
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
            # print("datesetter_generic else clause",placeholder)
            strptime_format = placeholder.replace('yyyy', '%Y').replace('mm', '%m').replace('dd', '%d').replace('hh','%I').replace('mm','%M').replace('ss','%S').replace('(am|pm)', '%#p')
            # print(strptime_format)
            label = driver.find_element(By.XPATH,f"//label[@for='{key}']")
            # print('label',label.text)
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

def dropdown_selector(driver,key):
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

def fake_data_based_on_id(driver,key,json_data_1):
    fake = Faker('en_US') 
    
    for json_key, value in json_data_1.items():
        print(f"======>{key} : {json_key}<=========", value)
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
    
def click_link_by_text(driver, link_text):
    #print(f"Clicking on link with text '{link_text}'...")
    try:
        # Locate the link by its text and click it
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, link_text))
        )
        link.click()
        #print(f"Clicked on link with text '{link_text}'.")
    except TimeoutException:
        print(f"Timeout: Link with text '{link_text}' not found or not clickable.")
    except Exception as e:
        #print(f"Error while trying to click the link: {e}")
        pass
    finally:
        #print(f"Finished clicking on link with text '{link_text}'.")
        pass

def date_to_label_matcher(label):
    if label == 'calendar date entry':
        return datetime.today().date()
    
    if label == 'Year of Make *':
        date_new= fake.date_between(start_date='today', end_date='-10y')
        return date_new
    if label == 'Date of Birth':
        older_date = fake.date_time_between(start_date="-18y", end_date="-100y")

        return older_date
    else:
        return fake.date_time_this_decade()

   
def button_finder(driver,key):
    create_menu_loading_check = WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.XPATH,key)))
    section_elements = driver.find_elements(By.TAG_NAME, 'section')
    for section in section_elements:
        buttonlist = section.find_elements(By.TAG_NAME, 'button')
        listofitems = {}
        failed_inputs = 0
        multiple_drivers = False
        for button in buttonlist: 
            # key = button.get_attribute("id")
            text = button.text
            field_type = button.get_attribute("type")
            print(field_type)
         
            print(text)
            try:
                label = button.find_element(By.XPATH, "preceding-sibling::label")
                print(label.text)
                button.click()
                parent_element = label.find_element(By.XPATH, "..")
                following_sibling = parent_element.find_element(By.XPATH, "following-sibling::*")
                following_sibling.click()
            except:
                pass

#======================== peril related functions ========================================
def peril_matcher(driver,peril_list_json):
     Policy_details ='/html/body/div[1]/div[2]/div/div/div[2]/ul/li[1]'
     exposure_link='/html/body/div[1]/div[2]/div/div/div[2]/ul/li[2]'
     vehicle_link ='/html/body/div[1]/div[2]/div/div/div[2]/ul/li[2]/ul'
     peril_link ='/html/body/div[1]/div[2]/div/div/div[2]/ul/li[2]/ul/div/div/li/ul/div/div/li/div'
     LINK_A ='/html/body/div[1]/div[2]/div/div/div[2]/ul/li[2]/ul/div/div/li/ul/div/div/li/div/div[2]/div/div/a'

     vehicle_link_check = WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.XPATH,vehicle_link)))
     driver.find_element(By.XPATH,vehicle_link).click()     
     try:
         time.sleep(1)
         perils_check = WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.XPATH,peril_link)))
         driver.find_element(By.XPATH,peril_link).click()
         time.sleep(1)
         tbody = driver.find_element(By.TAG_NAME, 'tbody')
         perils = tbody.find_elements(By.XPATH, '//a[contains(@class, "MuiTableRow-root")]')
        #  print(len(perils))                
     except:
         pass
     
     for peril in perils:
        try:
            #checking the first peril element in the table
            perils_check = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div[2]/main/div/div/div[2]/div/div[3]/div/div/table/tbody/a[1]')))
            #peril row peril name extraction using innerHTML attribute
            peril_name = peril.find_element(By.XPATH,'./*[1]').get_attribute("innerHTML")
            for key, value in peril_list_json.items():
                if peril_name in key and value== False:
                    remove_container = peril.find_element(By.XPATH,'./*[3]')
                    remove_container.find_element(By.TAG_NAME,'a').click()
                    removebutton = WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.XPATH,f'//button[text()="Remove"]'))) 
                    driver.find_element(By.XPATH,f'//button[text()="Remove"]').click()
                    # time.sleep(2)
                    WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div[2]/main/div/div/div[1]/span/svg'))) 
                    WebDriverWait(driver,5).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[1]/span/svg')))
                    # time.sleep(2)
                    WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div[1]/div/div/div[2]'))) 
                    WebDriverWait(driver,5).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/div/div[2]')))
                    peril_matcher(driver,peril_list_json)                                        
                    # /div/span/svg
                    # /html/body/div[1]/div[1]/div/div/div[2]
                    # /html/body/div[1]/div[1]/div/div/button
        except:
            print('element not matched')

def peril_getter(driver):
            # Policy_details ='/html/body/div[1]/div[2]/div/div/div[2]/ul/li[1]'
            # exposure_link='/html/body/div[1]/div[2]/div/div/div[2]/ul/li[2]'
            vehicle_link ='/html/body/div[1]/div[2]/div/div/div[2]/ul/li[2]/ul'
            peril_link ='/html/body/div[1]/div[2]/div/div/div[2]/ul/li[2]/ul/div/div/li/ul/div/div/li/div'
            # LINK_A ='/html/body/div[1]/div[2]/div/div/div[2]/ul/li[2]/ul/div/div/li/ul/div/div/li/div/div[2]/div/div/a'

            vehicle_link_check = WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.XPATH,vehicle_link)))
            driver.find_element(By.XPATH,vehicle_link).click()     
            try:
                time.sleep(1)
                perils_check = WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.XPATH,peril_link)))
                driver.find_element(By.XPATH,peril_link).click()
                time.sleep(1)
                tbody = driver.find_element(By.TAG_NAME, 'tbody')
                perils = tbody.find_elements(By.XPATH, '//a[contains(@class, "MuiTableRow-root")]')
                return perils                
            except:
                print(f'peril getter failed')
         
def peril_deleter(driver,perils,peril_list_json):
    for peril in reversed(perils):
        pass
# /html/body/div[1]/div[2]/main/div/div/div[1]/span/svg

def peril_setter(driver,perils,peril_list_json):

    for peril in reversed(perils):
        pass

         





def accordian_filler():
    pass








if __name__ =="__main__":
    print("...")