# 1: Webscraper
# This script outputs a .csv file of Examples and their relevant Techniques from the MITRE ATT&CK website
# One improvement to make could be to extract sub techniques' examples and plunk them under the main technique

import re
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Mac: webdriver.Chrome(service=Service("<path to chromedriver>"))
# Windows: webdriver.Chrome(executable_path=r"<path to chromedriver")
# Linux: webdriver.Chrome(service=Service("<path to chromedriver>"))
driver = webdriver.Chrome(service=Service("/home/intern/Documents/Jewel/text_classification/chromedriver/chromedriverlinux"))

# MITRE ATT&CK Techniques: main_techn (known as tactic) > techn > sub_techn

# outputs a dictionary of {Techn_num: Techn_name}
def get_techn_names(driver, techn_num):
    techn_names = driver.find_elements(By.XPATH, "//*[@class='technique']/td[2]")
    techn_names_dict = {}
    techn_names_list = []
    for i in range(len(techn_names)):
        techn_names_list.append(techn_names[i].text)
        techn_names_dict[techn_num] = techn_names_list
    return techn_names_dict

# outputs a dictionary of {Subtechn_num: Subtechn_name}
def get_subtechn_names(driver, techn_num):
    subtechn_names = driver.find_elements(By.XPATH, "//*[@class='sub technique']/td[3]")
    subtechn_names_dict = {}
    subtechn_names_list = []
    for i in range(len(subtechn_names)):
        subtechn_names_list.append(subtechn_names[i].text)
        subtechn_names_dict[techn_num] = subtechn_names_list
    return subtechn_names_dict

all_main_techn_dict = {}
all_techn_dict = {}
all_subtechn_dict = {}

# for multiple techniques
# change range to get different techniques
# main_techn_num = ['08', '09']
# for i in main_techn_num:

# for only 1 technique (write techn_num in str())
if True == True:
    techn_num = 'TA' + '00' + str("01") # replace str() with i if multiple techniques
    url = 'https://attack.mitre.org/tactics/' + techn_num
    driver.get(url)

    main_techn = driver.find_elements(By.TAG_NAME, 'h1')
    main_techn_dict = {}
    for t in range(len(main_techn)):
        main_techn_dict[techn_num] = main_techn[t].text
        all_main_techn_dict.update(main_techn_dict)

    techn_names_dict = get_techn_names(driver, techn_num)
    all_techn_dict.update(techn_names_dict)

    subtechn_names_dict = get_subtechn_names(driver, techn_num)
    all_subtechn_dict.update(subtechn_names_dict)
    
# all_main_techn_dict is {T000XX: "Main Technique"}
# all_techn_dict is {T000XX: ["Technique1", "Technique 2"]}
# all_subtechn_dict is {T000XX: ["SubTechnique1", "SubTechnique 2"]}

# clicking into the links of the techniques and extracting examples for each technique
all_examples_dict = {}
for k in all_techn_dict:
    driver.get(f'https://attack.mitre.org/tactics/{k}/')
    techn_id_name = all_main_techn_dict[k]
    print(f"Generating {techn_id_name}'s techniques now...")
    # value in all_techn_dict is a list of the techniques in one main technique
    for d in all_techn_dict[k]:
        # d is the name of each technique under a tactic
        techn_link = driver.find_element(By.LINK_TEXT, d)
        techn_link.click()
        
        if len(driver.find_elements(By.ID, "examples"))>0: # checking if "Procedure Example" exists
            examples = driver.find_elements(By.XPATH, "//*[@class='table table-bordered table-alternate mt-2'][1]/tbody/tr/td[3]")
            tech_id_raw = driver.find_element(By.XPATH, "//div[@class='col-md-11 pl-0']").text
            tech_id = tech_id_raw.replace("ID: ", "")
        else:
            # skipping techniques with no examples
            continue
        
        examples_list = []
        examples_dict = {}
        for i in range(len(examples)):
            example_text = examples[i].text
            example_new_text = re.sub(r'\[\d{1,3}\]','', example_text) # to remove the [] references in text
            examples_list.append(example_new_text)
        examples_dict[techn_id_name + ": " + tech_id + " " + d] = examples_list
        all_examples_dict.update(examples_dict)

        driver.back()
    print(f"Completed generation of {techn_id_name}'s techniques.")
driver.close()
# all_examples_dict will combine ALL main technique's {Technique: ['Example1', 'Example2']}

# output to new csv file 'training.csv'
with open(os.path.join("assets","training.csv"), 'w', encoding="utf8", newline='') as csvfile:
    headings = ['Technique', 'Example']
    new_val = csv.DictWriter(csvfile, fieldnames=headings)
    new_val.writeheader()

    for k,v in all_examples_dict.items():
        for i in v:
            new_val.writerow({'Technique': k, 'Example': i})