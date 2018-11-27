import getpass
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from utilities import check_continue, css_select, is_url

# Initialize the driver #
driver = webdriver.Chrome()
actions = ActionChains(driver)

home_url = 'https://marketingplatform.google.com/home/orgs/0e--yVH2TwO9v2yGo4zETQ/settings?authuser=0'
driver.get(home_url)

# Globals #
email_list = [
        'tyler.duddy@jellyfish.net',
        'drew.forster@jellyfish.net',
        'nick.pratzer@jellyfish.net',
        'olade.honvo@jellyfish.co.uk'
    ]

group_list = [
        'selenium_test_1',
        'selenium_test_2',
        'selenium_test_3',
        'selenium_test_4'
    ]

# Program Functions #
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

def create_user_group(group_name, email_list, permission_level):
    user_group_btn_css = 'gap-navigation-slat.um-groups-slat section.gaux-slat-button.gap-navigation-slat div div.gap-navigation-slat-content:nth-child(2) span:nth-child(1)'
    user_group_btn = css_select(user_group_btn_css, driver=driver)
    user_group_btn.click()
    
    sleep(0.5)

    add_group_btn_css = 'button[aria-label="Create new group"]'
    add_group_btn = css_select(add_group_btn_css, driver=driver)
    add_group_btn.click()
    
    group_name_input_css = 'input[placeholder="Name"]'
    group_name_input = css_select(group_name_input_css, driver=driver)
    group_name_input.send_keys(group_name)
    group_name_input.send_keys(u'\ue007') # unicode for ENTER key
    
    add_members_btn_css = 'um-group-members-slat'
    for i in range(10):
        try:
            add_members_btn = css_select(add_members_btn_css, driver=driver)
            break
        except:
            sleep(0.5)
    add_members_btn.click()

    sleep(0.5)

    add_member_plus = css_select('button[aria-label="Add group members"]', driver=driver)
    add_member_plus.click()

    sleep(0.5)

    email_input = css_select('input[aria-label="Input user email addresses"]', driver=driver)
    for email in email_list:
        email_input.send_keys(email + " ")
        sleep(0.5)
    
    actions.move_to_element_with_offset(driver.find_element_by_tag_name('body'), 0,0)
    actions.move_by_offset(1112, 19).click().perform()

    for i in range(3):
        actions.move_to_element_with_offset(driver.find_element_by_tag_name('body'), 0,0)
        actions.move_by_offset(50, 100).click().perform()
        sleep(0.5)

def main():
    sign_in()
    for group_name in group_list:
        create_user_group(group_name, email_list,'')
    check_continue(driver=driver)

if __name__ == "__main__":
    main()
