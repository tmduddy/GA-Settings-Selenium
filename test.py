from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import re

from utilities import *

# Initialize the driver
driver = webdriver.Chrome()

driver.get('https://analytics.google.com')
sign_in(driver)

my_list = list_from_csv('data/loreal-spain-accounts.csv', 3)[1:]
for name in my_list:
    print(name)
    print(url_from_id(name,need_primary_view=True, driver=driver))
    check_continue(driver=driver)
