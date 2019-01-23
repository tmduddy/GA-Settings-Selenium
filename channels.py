from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import re

from utilities import *

# Initialize the driver
driver = webdriver.Chrome()

# if running the project non-locally, you'll need to input the full path to the directory here
# ex. /home/username/dev/selenium-test/
project_path = ''

def delete_all_channels(id_params):
    # navigate to default channel grouping
    sleep(1)
    driver.get('https://analytics.google.com/analytics/web/#/{}/admin/channel-grouping/m-content-channelGroupingTable.rowShow=10&m-content-channelGroupingTable.rowStart=0&m-content-channelGroupingTable.sortColumnId=aggregated&m-content-channelGroupingTable.sortDescending=true&m-content.mode=EDIT&m-content.groupId=0&m-content.groupType=CHANNEL'.format(id_params))
    
    # wait for the iframe to load and then switch focus to it
    sleep(2)
    iframe = is_element('#galaxyIframe', time=6, driver=driver)
    driver.switch_to.frame(iframe)

    # loop through all available delete buttons and confirm (validate that delete button would receive the click)
    delete = is_element('.ACTION-deleteRule', time=6, multiple=True, driver=driver)
    for element in delete:
        for i in range(8):
            try:
                element.click()
                break
            except:
                print(f"couldn't click delete in {i} tries")
                sleep(0.5)
        confirm = is_element('input[value="Delete Rule"]', time=4, driver=driver)
        confirm.click()

def read_channel_defs(file_name):
    name = []
    default = []
    rules_global = []
    rules_additional = []

    # Read the spreadsheet, skipping the first 4 rows, making 4 lists.
    with open(project_path + 'data/' + file_name, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i>4:
                name.append(row[1])
                default.append(row[2])
                rules_global.append(row[3])
                rules_additional.append(row[5])

    return [name, default, rules_global, rules_additional]

def update_channels(channel_defs):
    
    # loop through each definition
    for i in range(len(channel_defs[0])):
        channel = [channel_defs[0][i], channel_defs[1][i], channel_defs[2][i], channel_defs[3][i]]

        # "add a new channel" interactions
        add_new = is_element('._GAor', time=4, driver=driver)
        add_new.click()
        channel_name = is_element('.ID-ruleName', time=2, driver=driver)
        channel_name.send_keys(channel[0])
        sleep(0.5) # ensures that the word is fully typed

        rule_dropdown = is_element('[data-name="ID-conceptPickerMenuButton"]', time=2, driver=driver)
        rule_dropdown.click()

        # if the "Default" field is not blank, make the proper default settings, looking up the name of the channel
        if channel[1] != '':
            system_def = is_element('[class*="builtin_traffic_channel', time=4, driver=driver)
            system_def.click()
            matches_dropdown = is_element('[data-name="ID-enumValueSelector"]', time=2, driver=driver)
            matches_dropdown.click()

            defaults = {
                'Direct': '0',
                'Organic Search': '1',
                'Social & Influencer': '7',
                'Email': '3',
                'Affiliation': '6',
                'Referral': '2',
                'Paid Search': '4',
                'Display': '8',
                'Other Advertising': '5' 
            }

            value = defaults[channel[0]]
            matches_selection = is_element('[data-value="{}"]'.format(str(value)), time=2, driver=driver)
            matches_selection.click()

        # if the global definition is blank go to the next channel
        if channel[2] == '':
            done = is_element('.ACTION-finishRuleEdit', time=2, driver=driver)
            done.click()
            continue
        if channel[1] != '':
            #if there's already a system defined, use the OR button
            or_btn = is_element('[class*="ACTION-add-or"]', time=2, driver=driver)
            or_btn.click()

        # choose the first or second drop down depending on number of definitions needed
        if channel[1] == '':
            dropdown_css = '[data-name="ID-conceptPickerMenuButton"]'
        else:
            dropdown_css = 'div.ID-condition-0-1 > div > button'

        # apply the global rules
        global_dropdown = is_element(dropdown_css, time=4, driver=driver)            
        global_dropdown.click()

        medium = is_element('[class*="TARGET-analytics.medium"]', time=2, driver=driver)
        medium.click()

        match_type = is_element('[data-name="ID-matchTypeSelector"]', time=4, driver=driver)
        match_type.click()

        # choose the proper match type
        if re.match(r".*exactly matches.*", channel[2]):
            selector = is_element('[data-value="include-EQ"]', time=2, driver=driver)
        elif re.match(r".*matches regex.*", channel[2]):
            selector = is_element('[data-value="include-RE"]', time=2, driver=driver)
        elif re.match(r".*contains.*", channel[2]):
            selector = is_element('[data-value="include-PT"]', time=2, driver=driver)

        selector.click()

        expression_box = is_element('[data-name="ID-expression"]', time=2, driver=driver)

        expression_list = channel[2].split(' ')
        expression = ' '.join(expression_list[4:]) if expression_list[0] == 'OR' else ' '.join(expression_list[3:])
        expression_box.send_keys(expression)
        sleep(0.25) # ensure that the full pattern is typed
        # click done and save
        done = is_element('.ACTION-finishRuleEdit', time=2, driver=driver)
        done.click()
    save = is_element('[value="Save"]', time=2, driver=driver)
    save.click()
    close_button = is_element('[class*="ID-closeButton"]', 3, False, driver=driver)
    try:
        close_button.click()
    except:
        print('no close button to click')
    driver.switch_to.default_content()

def main():
    ids = list_from_csv('data/loreal-argentina-accounts.csv', 4)[1:]
    for id in ids:
        id_params = url_from_id(id, False, driver=driver)
        delete_all_channels(id_params)

        channel_defs = read_channel_defs('loreal-argentina-channels.csv')

        update_channels(channel_defs)

    print('done all channels')
    check_continue(driver=driver)

if __name__ == "__main__":
    driver.get('https://analytics.google.com')
    sign_in(driver)
    executor_url = driver.command_executor._url
    session_id = driver.session_id
    print(f"sess_id = {session_id}")
    print(f"exe_url = {executor_url}")
    while(True):
        try:
            main()
        except Exception as e:
            print(e)
            check_continue("TRY AGAIN? y/n ",driver=driver)