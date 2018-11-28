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
