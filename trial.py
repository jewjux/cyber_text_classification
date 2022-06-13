from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

driver = webdriver.Chrome('C:\Users\user\Downloads\chromedriver_win32\chromedriver.exe')

#main_techn, techn, sub_techn

def get_tech_names (driver):
    # getting the path for the tech_names
    
    
    # getting the number of rows
    num_rows = len(driver.find_elements_by_xpath("//*[@id='customers']/tbody/tr"))


for techn in (8, 10):
    page_num = 'TA' + str(000) + str(techn)
    url = 'https://attack.mitre.org/tactics/' + page_num
    driver.get(url)

    main_techn_names = driver.find_element(By.TAG_NAME, 'h1')

    