from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import re

from utilities import *

# Initialize the driver
driver = webdriver.Chrome()

# if running the project non-locally, you'll need to input the full path to the directory here
# ex. /home/username/dev/selenium-test/
project_path = ''

def navigate_to_dv_linking(id_params, dv_id):
    sleep(3)
    driver.get(f'https://analytics.google.com/analytics/web/#/{id_params}/admin/integrations/dbm-linksv2/table')

    current_dv_id = is_element('td[ng-bind="::rowData.advertiserId"]',time=10, driver=driver).text
    is_match = (current_dv_id == dv_id)
    print(f'match = {is_match}\n')

    if not is_match:
        return (id_params, dv_id)

def main():
    problem_id_params = []
    problem_dv_ids = []

    all_files = get_file_names("accounts")
    for file_name in all_files:
        ac_ids = list_from_csv(f'data/{file_name}', 5)[1:]
        dv_ids = list_from_csv(f'data/{file_name}', 1)[1:]

        print(f"***{file_name}***")
        for ac_id, dv_id in zip(ac_ids, dv_ids):
            if len(dv_id) <= 1:
                continue
            try:
                id_params = url_from_id(ac_id, False, driver=driver)
            except Exception as e:
                print(e)
                continue_button = is_element('ga-dialog-buttons-ok', 3, driver=driver)
                continue_button.click()
                continue
            check = navigate_to_dv_linking(id_params, dv_id)
            if not check:
                continue
            # if it doesn't match, append the idparams and required ID to a list
            problem_id_params.append(check[0])
            problem_dv_ids.append(check[1])
        
    print(problem_id_params)
    print(problem_dv_ids)
    print(f'number of problem ids = {len(problem_id_params)}')


if __name__ == "__main__":
    driver.get('https://analytics.google.com')
    sign_in(driver=driver)
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        check_continue(driver=driver)