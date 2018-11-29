import getpass
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def css_select(selector, multiple=False, driver=''):
    if multiple:
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

def is_element(css, time=1, driver=''):
    for i in range(time*10):
        try:
            return css_select(css, driver=driver)
        except:
            sleep(0.5)

def sign_in(driver):
    email_field = css_select('[type="email"]', driver=driver)
    username = "tyler.duddy@jellyfish.net"

    email_field.send_keys(username)
    email_field.send_keys(u'\ue007') # unicode for ENTER key
    
    sleep(1) #need to wait for the password field to exist
    
    pass_field = css_select('[type="password"]', driver=driver)
    password = getpass.getpass()
    pass_field.send_keys(password)
    pass_field.send_keys(u'\ue007') # unicode for ENTER key
    
    check_continue("Is the page resolved? y/n: ", driver=driver)
