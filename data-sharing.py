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

# if running the project non-locally, you'll need to input the full path to the directory here
# ex. /home/username/dev/selenium-test/
project_path = ''

# PROGRAM FUNCTIONS #
def block_data_sharing(idparams):
    sleep(4)
    print('ID Params: {}'.format(idparams))
    new_url = "https://analytics.google.com/analytics/web/#/{}/admin/account/settings".format(idparams)
    driver.get(new_url)
    sleep(1)
    if not is_url(new_url, 4, driver=driver): 
        print("didn't get to settings")
        return

    checkboxes = is_element('[role="checkbox"]', 3, multiple=True, driver=driver)

    # uncheck all data_sharing boxes.
    for box in checkboxes:
        box_class = box.get_attribute('class')
        if 'checked' in box_class:
            box.click()
        else:
            continue
    
    # save and print confirmation
    save_button = is_element('[type="submit"]', 2, driver=driver)
    save_button.click()
    print("Finished blocking data sharing, moving on\n")

def url_from_id(id, id_type="view"):
    print('headed to ID: {}'.format(str(id)))
    dropdown = is_element('button[aria-label="Open the universal picker."]', driver=driver)
    dropdown.click()
    search_box = is_element('input[suite-header-gtm-action="Search Universal Picker"]', 2, driver=driver)
    #search_box.click()
    # wrap search typing in sleeps to allow all of the text to type
    sleep(0.5)
    search_box.send_keys(str(id))
    sleep(0.5)
    result = is_element('a.suite-detailed-entity-list-row', 4, driver=driver)
    result.click()
    url = str(driver.current_url).split('/')
    if "admin" in url:
        return url[6]
    else: return url[7]

# MAIN # 
def main():
    driver.get('https://analytics.google.com')
    sleep(0.2)

    # check for sign-in page
    current_url = driver.current_url
    if("accounts.google.com/signin/v2/identifier" in current_url):
        sign_in(driver=driver)

    # get ids from spreadsheet, ditching second row of headers
    ids = list_from_csv(project_path + 'data/loreal-spain-accounts.csv', 3)[1:]
    for id in ids:
        if len(id) <= 4:
            continue
        idparams = url_from_id(id)
        block_data_sharing(idparams)
    
    check_continue('Done, enter "y" to exit: ', driver=driver)     
    driver.quit()


if __name__ == '__main__':
    try:
        main()
    finally:
        driver.quit()