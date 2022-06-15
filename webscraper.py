from selenium import webdriver
from selenium.webdriver.common.by import By
<<<<<<< Updated upstream
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import csv

driver = webdriver.Chrome(executable_path=r"C:\Users\user\Desktop\text_classification\chromedriver.exe")
=======
import re
import csv

# Mac: webdriver.Chrome(service=Service("/Users/jewel/Documents/text_classification/chromedrivermac"))
# Windows: webdriver.Chrome(executable_path=r"C:\Users\user\Desktop\text_classification\chromedriverwindows.exe")
driver = webdriver.Chrome(executable_path=r"C:\Users\user\Desktop\text_classification\chromedriverwindows.exe")
>>>>>>> Stashed changes

# main_techn, techn, sub_techn

def get_techn_names(driver, techn_num):
    techn_names = driver.find_elements(By.XPATH, "//*[@class='technique']/td[2]")
    techn_names_dict = {}
    techn_names_list = []
    for i in range(len(techn_names)):
        techn_names_list.append(techn_names[i].text)
        techn_names_dict[techn_num] = techn_names_list
    return techn_names_dict

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

# change range to get different techniques
<<<<<<< Updated upstream
for i in (8, 9):
    techn_num = 'TA' + '000' + str(i)
=======
main_techn_num = (8, 9)

# for only 1 technique
if True == True:

#for i in main_techn_num:
    techn_num = 'TA' + '000' + str(8)
>>>>>>> Stashed changes
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

all_examples_dict = {}
# clicking into the links of the techniques
for k in all_techn_dict:
    driver.get(f'https://attack.mitre.org/tactics/{k}/')
    techn_id_name = all_main_techn_dict[k]
    print(f"Generating {techn_id_name}'s techniques now...")
    # value is a list of the techniques in one main technique
    for d in all_techn_dict[k]:
        # d is the name of the technique
        techn_link = driver.find_element(By.LINK_TEXT, d)
        techn_link.click()
        
<<<<<<< Updated upstream
        # checking if "Procedure Example" exists
        if len(driver.find_elements(By.ID, "examples"))>0:
            examples = driver.find_elements(By.XPATH, "//*[@class='table table-bordered table-alternate mt-2']/tbody/tr/td[3]")
=======
        if len(driver.find_elements(By.ID, "examples"))>0: # checking if "Procedure Example" exists
            examples = driver.find_elements(By.XPATH, "//*[@class='table table-bordered table-alternate mt-2'][1]/tbody/tr/td[3]")
            tech_id_raw = driver.find_element(By.XPATH, "//div[@class='col-md-11 pl-0']").text
            tech_id = tech_id_raw.replace("ID: ", "")
>>>>>>> Stashed changes
        else:
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
    print(f"Completed searching for {techn_id_name}'s techniques.")
driver.close()

# all_examples_dict will output combine ALL main technique's {Technique: ['Example1', 'Example2']}

# converting to csv file
'''
with open('training.csv', 'w', newline='') as csvfile:
    headings = ['Technique', 'Example']
    new_val = csv.DictWriter(csvfile, fieldnames=headings)

    new_val.writeheader()
    for k in all_examples_dict:
        new_val.writerow({'Technique': k, 'Example': all_examples_dict[k]})
'''




    