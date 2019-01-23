import getpass
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from utilities import *

# Initialize the driver
driver = webdriver.Chrome()

# if running the project non-locally, you'll need to input the full path to the directory here
# ex. /home/username/dev/selenium-test/
project_path = 'data/'

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



# MAIN # 
def main():
    driver.get('https://analytics.google.com')
    sleep(0.2)

    # check for sign-in page
    current_url = driver.current_url
    if("accounts.google.com/signin/v2/identifier" in current_url):
        sign_in(driver=driver)

    for file_name in get_file_names('accounts'):
        # get ids from spreadsheet, ditching second row of headers
        print(f'***{file_name}***')
        ids = list_from_csv(project_path + file_name, 5)[1:]
        for id in ids:
            if len(id) <= 4:
                continue
            try:
                idparams = url_from_id(id, driver=driver)
                block_data_sharing(idparams) 
            except Exception as e:
                print(f'COULD NOT VALIDATE {id}\n')
                print(e)
                continue

if __name__ == '__main__':
    try:
        main()
    finally:
        driver.quit()