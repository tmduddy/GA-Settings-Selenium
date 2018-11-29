import getpass
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from utilities import check_continue, css_select, is_element, is_url, sign_in

# Initialize the driver #
driver = webdriver.Chrome()
actions = ActionChains(driver)

home_url = 'https://marketingplatform.google.com/home/orgs/0e--yVH2TwO9v2yGo4zETQ/settings?authuser=0'
driver.get(home_url)

# Globals #
email_list = [
        'tyler.duddy@jellyfish.net',
        'drew.forster@jellyfish.net',
        'olade.honvo@jellyfish.co.uk'
    ]

group_list = [
        'selenium_test_1',
        'selenium_test_2',
    ]

# Program Functions #
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
    add_members_btn = is_element(add_members_btn_css, driver=driver)
    add_members_btn.click()

    add_member_plus_css = 'button[aria-label="Add group members"]'
    add_member_plus = is_element(add_member_plus_css, driver=driver)
    add_member_plus.click()

    email_input_css = 'input[aria-label="Input user email addresses"]'
    email_input = is_element(email_input_css, driver=driver)
    
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
    sign_in(driver)
    for group_name in group_list:
        create_user_group(group_name, email_list,'')
    check_continue(driver=driver)

if __name__ == "__main__":
    main()
