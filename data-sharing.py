import getpass
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from utilities import *

# Initialize the driver
driver = webdriver.Chrome()

# GLOBALS #
URLS = [
    'a118991582w176240649p175113216',
    'a118991582w176240649p175124888'
]

# PROGRAM FUNCTIONS #
def block_data_sharing(id_params):
    url = f'https://analytics.google.com/analytics/web/#/{id_params}/admin/account/settings'
    driver.get(url)
    if not is_url(url, driver=driver): return
    checkboxes = driver.find_elements_by_css_selector('[role="checkbox"]')

    # check to make sure there are checkboxes on the page
    for i in range(20):
        if len(checkboxes) != 0:
            break
        checkboxes = css_select('[role="checkbox"]', multiple=True, driver=driver)
        sleep(0.1)
        
    # ensure that boxes 0, 1, 3, 4 are unchecked and box 2 is checked
    for i in range(len(checkboxes)):
        check_box = checkboxes[i]
        check_class = check_box.get_attribute('class')
        if 'checked' in check_class and i != 2:
            check_box.click()
        elif 'checked' not in check_class and i==2:
            check_box.click()
        else:
            continue
        
    save_button = css_select('[type="submit"]', driver=driver)
    save_button.click()
    print("Finished blocking data sharing, moving on")

# MAIN # 
def main():
    driver.get('https://analytics.google.com')
    sleep(0.2)
    current_url = driver.current_url
    if("accounts.google.com/signin/v2/identifier" in current_url):
        sign_in(driver=driver)

    for id_params in URLS:
        block_data_sharing(id_params)

    check_continue('Done, enter "y" to exit: ', driver=driver)     
    driver.quit()


if __name__ == '__main__':
    main()
