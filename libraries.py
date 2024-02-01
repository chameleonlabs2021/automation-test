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






def login_to_socotra (driver):
    # Create a Chrome webdriver

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


# Configuration loading function
def load_config(driver, path):
    #print("Starting load_config function...")
    try:
        csv_file_path = path
        data_list = read_data_from_csv(csv_file_path)

        # Define the regex pattern
        regex_pattern = "policyholder\.tenant_[a-z0-9]+_{}"

        # Iterate through the list of data and fill in the fields
        all_fields_successful = True
        for item in data_list:
            title = item['title']
            data_to_input = item['data']
            field_type = item['type']
            switch = item['switch']
            specific_pattern = regex_pattern.format(re.escape(title))

            if field_type == 'select':
                # success = handle_custom_dropdown(driver, title, data_to_input, specific_pattern)
                # success= find_element_with_dynamic_id(driver, specific_pattern)
                # Usage
                end_id = title
                success = click_and_select_by_id_ending_with(driver, end_id, data_to_input)
                #print(f"Found element: {success}")
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
                #print(f"Failed to interact with field with title: {title}")
                all_fields_successful = False
                break  # Exit the loop if a field interaction fails

        #print("Ending load_config function...")
        return all_fields_successful        
    except Exception as e:
        #print(f"Error in load_config function: {e}")
        return False

def handle_input_or_select(driver, title, text_to_input, pattern):
    #print(f"Starting handle_input_or_select function for field '{title}'...")
    try:
        element = find_element_by_regex_title(driver, title, pattern)
        #print(f"Found element: {element}")

        # Check if the element is a dropdown
        element.clear()
        element.send_keys(text_to_input)

        #print(f"Ending handle_input_or_select function for field '{title}'...")
        return True
    except Exception as e:
        #print(f"Failed to find or interact with the element: {e}")
        #print(f"Ending handle_input_or_select function for field '{title}'...")
        return False

def interact_with_field(driver, item, regex_pattern):
    #print(f"Starting interact_with_field function for field '{item['title']}'...")
    """
    Interacts with a field based on its type, title, and data.

    :param driver: Selenium WebDriver instance.
    :param item: Dictionary containing title, data, and type of the field.
    :param regex_pattern: Pattern to generate specific field ID or locator.
    :return: True if interaction was successful, False otherwise.
    """
    title = item['title']
    data_to_input = item['data']
    field_type = item['type']
    specific_pattern = regex_pattern.format(re.escape(title))

    try:
        if field_type == 'select':
            end_id = title  # Modify as needed
            click_and_select_by_id_ending_with(driver, end_id, data_to_input)
        elif field_type == 'date':
            set_date_field(driver, title, specific_pattern, data_to_input)
        else:
            handle_input_or_select(driver, title, data_to_input, specific_pattern)
        return True
    except Exception as e:
        #print(f"Failed to interact with field '{title}' of type '{field_type}': {e}")
        return False
    finally:
        #print(f"Ending interact_with_field function for field '{item['title']}'...")
        pass

   
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



# def read_data_from_csv(file_path):
#     data_list = []
#     with open(file_path, newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             data_list.append({
#                 'title': row['title'].strip(),
#                 'data': row['data'].strip(),
#                 'type': row['type'].strip()
#             })
#     return data_list

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




def vehicle_string_field_by_id_ending_with(driver, end_id, text_to_input):
    #print(f"Starting vehicle_string_field_by_id_ending_with for end_id: {end_id}...")
    try:
        # Construct an XPath that checks if the ID ends with end_id
        element_xpath = f"//input[contains(@id, '{end_id}')]"
        #print(f"Checking if element with XPath: {element_xpath} exists")
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, element_xpath))
        )
        element.clear()
        element.send_keys(text_to_input)
        #print(f"Clicked element: {element}")
        return True
    except Exception as e:
        #print(f"Error during vehicle_string_field_by_id_ending_with: {e}")
        raise
    finally:
        #print(f"Ending vehicle_string_field_by_id_ending_with for end_id: {end_id}...")
        pass

def _vehicle_click_and_select_by_id_ending_with(driver, end_id, value_to_select):
    #print(f"Starting vehicle_click_and_select_by_id_ending_with for end_id: {end_id}...")
    try:
        # Construct an XPath that checks if the ID ends with end_id
        element_xpath = f"//input[contains(@id, '{end_id}')]"
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
        #print(f"Error during vehicle_click_and_select_by_id_ending_with: {e}")
        raise
    finally:
        #print(f"Ending vehicle_click_and_select_by_id_ending_with for end_id: {end_id}...")
        pass

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

def scroll_to_location(driver, type, element):
    #print("Starting scroll_to_location...")
    #print(element)
    #print(type)
    
    try:
        if type == 'ID':
            #print('Testing ID')
            scroll_location = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element)))
        elif type == 'XPATH':
            scroll_location = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, element)))
        driver.execute_script('arguments[0].scrollIntoView(true)', scroll_location)
        wait.until(is_scroll_complete)
    except Exception as e:
        #print(f"Error during scroll_to_location: {e}")
        pass
    finally:
        #print("Ending scroll_to_location...")
        pass

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


    
def field_filler(driver, key, field_type=None):
    
    try:
        
        key_lower = key.lower()

        if field_type == 'text':
            print(type(key_lower))
            if 'vin' in key_lower:
                print("key===>" ,key_lower)
                # fake_vin = fake.uuid4()[:17].upper()    
                fake_vin ='2HGFB2F59EH567890' ##TODO fix input hardcoded vin for now
                print("fake_vin===>",fake_vin)
                input_field = driver.find_element(By.ID, key)
                input_field.send_keys(fake_vin)
                #print(f"text field success {key}")
            else:    
                input_field = driver.find_element(By.ID, key)
                input_field.send_keys(fake.sentence())
                #print(f"text field success {key}")
        elif field_type == 'number' or 'number' in key_lower:
            input_field = driver.find_element(By.ID, key)
            input_field.send_keys(fake.random_number(digits=5))
            #print(f"number field success {key}")
        elif field_type == 'email' or 'email' in key_lower:
            input_field = driver.find_element(By.ID, key)
            input_field.send_keys(fake.email())
            #print(f"email field success {key}")
        elif field_type in ['telephone', 'phone'] or any(substring in key_lower for substring in ['phone', 'tel', 'hp', 'handphone']):
            input_field = driver.find_element(By.ID, key)
            input_field.send_keys(fake.phone_number())
            #print(f"phone field success {key}")
        elif 'year' in key_lower:
            input_field = driver.find_element(By.ID, key)
            input_field.send_keys(str(fake.year()))
            #print(f"year field success {key}")
        elif field_type == "tel":
            random_date = fake.date_time()
            input_feild = driver.find_element(By.ID,key)
            input_feild.send_keys(random_date.strftime("%Y/%m/%d %I:%M:%S %p"))
            #print(f"number feild success {key} ")      
        else:
            print(f"No specific data type matched for {key}")

    except Exception as e:
        pass
        # #print(f"Field {key} filling failed: {e}")

# def search_and_fill_all_dropdown_inputs(driver,scroll_to_location,wait):
    #print("Starting search_and_fill_all_dropdown_inputs...")
    inputlist = driver.find_elements(By.TAG_NAME, 'input')
    listofitems = {}
    failed_inputs = 0
    multiple_drivers = False
    for input_element in inputlist:
        key = input_element.get_attribute("id")
        #print("key", key)
        value = input_element.get_attribute("aria-autocomplete")
        #print("value", value)
        listofitems[key] = value
        try:
            dummycheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID, key)))
            driver.find_element(By.ID, key).click()
            link1 = (f"//ul[contains(@id,'{key}-listbox')]")
            ul_element = driver.find_element(By.XPATH, link1)
            li_elements = ul_element.find_elements(By.TAG_NAME, "li")
            selected_li = random.choice(li_elements)
            
            if key == "policyForm.multiple_drivers" and int(selected_li.get_attribute("data-option-index")) == 1:
                multiple_drivers = True
                #print("Multiple drivers selected")
            selected_li.click()
        except Exception as e:
            failed_inputs += 1
            # #print(f"Error for key {key}: {e}")
            pass
    items_filled = len(listofitems) - failed_inputs
    #print(f"Ending search_and_fill_all_dropdown_inputs. Items filled: {items_filled}, Multiple drivers: {multiple_drivers}")
    return listofitems, items_filled, multiple_drivers


def search_and_fill_all_dropdown_inputs(driver,scroll_to_location,wait,key):
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
        #print(f"{key} : {value}")
        try:
            dummycheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,key)))
            driver.find_element(By.ID,key).click()
            if value == 'list':
                dropdown_selector(driver,key)
            else:
                #print(f"elif hit")
                field_filler(driver,key,field_type)
        except:
            failed_inputs += 1
            # #print(key)
            pass

    items_filled = len(listofitems)- failed_inputs
    # #print(multiple_drivers)
    newelement = 'policy_id'
    scroll_to_location('ID',newelement)
    return listofitems, items_filled ,multiple_drivers


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

    except Exception as e:
        #print(f"Error while filling additional driver details: {e}")
        pass
    finally:
        #print("Ending additional_driver_details...")
        pass

def datesetter(driver, wait, page_scrolled_to_top):
    #print("Starting datesetter...")
    startdate = fake.date_between(start_date='today', end_date='+3y')
    enddate = fake.date_between(start_date='+3y', end_date='+30y')
    
    try:
        # Policy start date
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
        #print("Policy dates set successfully")
    except Exception as e:
        #print(f"Error while setting policy dates: {e}")
        pass
    finally:
        #print("Ending datesetter...")
        pass

def application_type_selector(driver,product = 1):   
    try:
      #to make sure the form is loaded by checking if first name feild is loaded 
      dummycheck = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/div[1]/div[2]/main/div/div[1]/div/a")))
      startbutton = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/main/div/div[1]/div/a")
      startbutton.click()
    except:
      #print("Url not loaded")
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
      #print("application dropdown selection and submission failed")
      driver.quit() 

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






if __name__ =="__main__":
    print("...")