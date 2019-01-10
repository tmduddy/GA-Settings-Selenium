from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from utilities import *

# Initialize the driver
driver = webdriver.Chrome()

# if running the project non-locally, you'll need to input the full path to the directory here
# ex. /home/username/dev/selenium-test/
project_path = ''


def main():
    driver.get('https://analytics.google.com')
    sign_in(driver)

    id_params = 'a118991582w176153053p175123642'

    driver.get('https://analytics.google.com/analytics/web/#/{}/admin/channel-grouping/m-content-channelGroupingTable.rowShow=10&m-content-channelGroupingTable.rowStart=0&m-content-channelGroupingTable.sortColumnId=aggregated&m-content-channelGroupingTable.sortDescending=true&m-content.mode=EDIT&m-content.groupId=0&m-content.groupType=CHANNEL'.format(id_params))
    
    sleep(2)
    iframe = is_element('#galaxyIframe', time=4, driver=driver)
    driver.switch_to.frame(iframe)
    delete = is_element('.ACTION-deleteRule', time=8, multiple=True, driver=driver)
    print(delete)
    delete[0].click()
    confirm = is_element('input[value="Delete Rule"]', time=4, driver=driver)
    confirm.click()
    
    # channel_group = is_element('.app-admin-channel-grouping', time=4, driver=driver)
    # channel_group.click()
    # channel_group = is_element('a[ui-sref="app.admin.channel-grouping"]', time=4, driver=driver)
    # channel_group.click()
    # channel_group = is_element('._GAEj', time=4, driver=driver)
    # channel_group.click()

    



    check_continue(driver=driver)




if __name__ == "__main__":
    try:
        main()
    finally:
        pass#driver.quit()