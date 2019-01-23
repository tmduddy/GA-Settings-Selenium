from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import re

from utilities import *

# Initialize the driver
driver = webdriver.Chrome()

# if running the project non-locally, you'll need to input the full path to the directory here
# ex. /home/username/dev/selenium-test/
project_path = ''