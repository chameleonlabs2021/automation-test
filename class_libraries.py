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







# generic selenium function class======================================================


class generic_functions:

    def __init__(self,driver) -> None:
        self.driver = driver


    def is_page_loaded(self):
        return self.driver.execute_script("return document.readyState === 'complete';")

    def button_clicker(self,button_id):
        print(button_id)
        try:
            if button_id.startswith('/'):# checking if the button id received is Xpath or id
                create_menu_loading_check = WebDriverWait(self.driver,15).until(EC.presence_of_all_elements_located((By.XPATH,button_id)))
                self.driver.find_elements(By.XPATH, button_id).click()
            else:
                create_menu_loading_check = WebDriverWait(self.driver,15).until(EC.presence_of_all_elements_located((By.ID,button_id)))
                self.driver.find_element(By.ID, button_id).click()
        except:
            print('create button click failed')

class socotra_functions:
     def __init__(self,driver) -> None:
        self.driver = driver
        

     def login_to_socotra (self, username,password, hostname,login_url):
        # Replace with the actual URL to login
        
        self.driver.get(self.login_url)
        person1 = "7e22ad18-4382-4455-8022-2ea631872f8c"
        # 522855ef-1536-410b-b4a6-a425f7c03723
        policy_holder_url = f"https://sandbox.socotra.com/policyholder/{person1}"

        # https://sandbox.socotra.com/policyholder/7e22ad18-4382-4455-8022-2ea631872f8c/overview
        # Fill in the login details
        self.driver.find_element(By.ID,"LoginForm__UsernameField--Standard").send_keys("alice.lee") 
        self.driver.find_element(By.ID,"LoginForm__PasswordField--Standard").send_keys("socotra") 
        self.driver.find_element(By.ID,"LoginForm__HostnameField--Standard").send_keys("rpoolanchalil-synpulse-configeditor.co.sandbox.socotra.com") 
        self.driver.find_element(By.ID, "LoginForm__Button--StandardLogin").click()
        # time.sleep(2) 
        # time.sleep(15) 

        #login page loaded check
        try:
            create_menu_loading_check = WebDriverWait(self.driver,15).until(EC.presence_of_all_elements_located((By.ID,'AppBar__Buttons--CreateDropdown')))
            
        except:
            #print("login failed or page not loaded properly")
            pass



            




























if __name__ =="__main__":
    print("Class_library")