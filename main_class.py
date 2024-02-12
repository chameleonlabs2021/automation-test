import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
import os
import time
from datetime import datetime
import random
from faker import Faker
from faker.providers import BaseProvider
from class_libraries import *
fake = Faker()
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# Create a Chrome webdriver
driver = webdriver.Chrome(options = chrome_options)
wait = WebDriverWait(driver, 10)
load_dotenv('test.env')

#======================= value comming fron ENV=======
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
hostname = os.getenv('HOSTNAME')
login_url = os.getenv('LOGIN_URL')

print(username)
test_instance = generic_functions(driver)
socotra_instance = socotra_functions(driver)

#login to socotra credintial hardcoded in the function/ credintial to be move to a ENV file
socotra_instance.login_to_socotra(username,password,hostname,login_url)



test_instance.button_clicker('AppBar__Buttons--CreateDropdown')


option1 ='CreateDropdown__ListItem--NewApplication'

option2 = 'CreateDropdown__ListItem--NewPolicyHolder'

test_instance.button_clicker(option1)




