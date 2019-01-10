import csv
import getpass
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def css_select(selector, multiple=False, driver=''):
    if multiple:
        if len(driver.find_elements_by_css_selector(selector)) > 0:
            return driver.find_elements_by_css_selector(selector)
    return driver.find_element_by_css_selector(selector)

def check_continue(prompt="continue? y/n: ", driver=''):
    is_continue = input(prompt)
    while True:
        if is_continue == 'y':
            return
        elif is_continue == 'n':
            driver.quit()
            quit()
        else:
            is_continue = input(f"invalid. {prompt}")

def is_url(url, time=1, driver=''):
    for i in range(time*10):
        if driver.current_url == url:
            print(f"ID\'d {url[38:]}")
            return True
        else:
            sleep(0.1)
    print(f"could not validate {url} within {time} seconds")
    return False

def is_element(css, time=1, multiple=False, driver=''):
    for i in range(time*2):
        try:
            return css_select(css, multiple, driver=driver)
        except:
            if i%2 != 0:
                print('Could not ID element: {} after {} tries'.format(css, str(i+1)))
            sleep(0.5)

def sign_in(driver):
    email_field = is_element('[type="email"]', driver=driver)
    username = "tyler.duddy@jellyfish.net"

    email_field.send_keys(username)
    email_field.send_keys(u'\ue007') # unicode for ENTER key
    
    # pass_field = is_element('[type="password"]', driver=driver)
    # password = getpass.getpass()

    # pass_field.send_keys(password)
    # pass_field.send_keys(u'\ue007') # unicode for ENTER key
    
    check_continue("Is the page resolved? y/n: ", driver=driver)

def list_from_csv(file_path, col_index):
    my_list = []
    with open(file_path) as csv_file:
        #reader gets assigned the content of the above csv file as value
        reader = csv.reader(csv_file)
        header = True
        for row in reader:
            #remove the first row or header
            if header:
                header = False
                continue
            # add the content of the given column to the list
            my_list.append(row[col_index])
        return my_list

def url_from_id(id, driver=''):
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
