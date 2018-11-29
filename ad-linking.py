def link_dv_360(id_params):
    url = f'https://analytics.google.com/analytics/web/#/{id_params}/admin/integrations/allproducts'
    driver.get(url)
    check_continue("Ready for product linking? y/n: ", driver=driver)
    print("Finished linker")