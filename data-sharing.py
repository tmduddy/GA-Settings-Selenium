import getpass
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from utilities import check_continue, css_select, is_url

# Initialize the driver
driver = webdriver.Chrome()

# GLOBALS #
URLS = [
    'a118991582w176240649p175113216',
    'a118991582w176240649p175124888'
]

# PROGRAM FUNCTIONS #
def sign_in():
    email_field = css_select('[type="email"]', driver=driver)
    #username = getpass.getpass('Username: ')
    username = "tyler.duddy@jellyfish.net"

    email_field.send_keys(username)
    email_field.send_keys(u'\ue007') # unicode for ENTER key
    
    sleep(1) #need to wait for the password field to exist
    
    pass_field = css_select('[type="password"]', driver=driver)
    password = getpass.getpass()
    pass_field.send_keys(password)
    pass_field.send_keys(u'\ue007') # unicode for ENTER key
    
    check_continue("Is the page resolved? y/n: ", driver=driver)
    
def block_data_sharing(id_params):
    print("Blocking data sharing")
    url = f'https://analytics.google.com/analytics/web/#/{id_params}/admin/account/settings'
    driver.get(url)
    if not is_url(url, driver=driver): return
    checkboxes = driver.find_elements_by_css_selector('[role="checkbox"]')
    # check to make sure there are checkboxes on the page
    tries = 0
    while len(checkboxes) == 0 and tries < 20:
        checkboxes = driver.find_elements_by_css_selector('[role="checkbox"]')
        sleep(0.1)
        tries += 1
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
        sign_in()

    for id_params in URLS:
        block_data_sharing(id_params)
        #link_dv_360(id_params)

    driver.get(f"https://analytics.google.com/analytics/web/#/{id_params}/admin/change-history/")
    while True:
        check_continue('Need more time? y/n: ', driver=driver)     
    driver.quit()


if __name__ == '__main__':
    main()
