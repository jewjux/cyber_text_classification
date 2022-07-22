# RU Actors Scraper
# Scraping the data for russian actors to get the paragraphs and techniques as training data

import os
import re
import json
import pandas as pd

with open(os.path.join("assets","ru_actors_reports.json"), 'r') as json_file:
	json_load = json.load(json_file)

extracted_dict = {}
reports_list = []
ttp_list = []
actor_list = []

# to check that all counts match as it will be number of rows in dataframe
count_report = 0
count_ttp = 0
count_actor = 0

for actor in json_load:
    for i in json_load[actor]:
        count_report += 1
        try:
            reports_list.append(i['description'])
        except:
            if 'description' not in i.keys() and "x_fireeye_com_additional_description_sections" in i.keys():
                # using analysis instead of report
                reports_list.append(i["x_fireeye_com_additional_description_sections"]["analysis"])
            else:
                # no report and no analysis
                reports_list.append("No report found.")

# checking if all entries in json was uploaded to list
if count_report == len(reports_list):
    extracted_dict["Reports"] = reports_list
else:
    print("Error: Not all reports were extracted.")

for actor in json_load:
    for i in json_load[actor]:
        count_ttp += 1
        try:
            ttp_list.append(i["x_fireeye_com_metadata"]["ttp"])
        except:
            if 'ttp' not in i["x_fireeye_com_metadata"].keys():
                ttp_list.append(["No ttp provided"])

for i in ttp_list:
    for ttp in i[:]:
        if bool(re.search(r'\d', str(ttp))):
            i.remove(ttp)
        if ttp == '':
            i.remove(ttp)
        if ttp == False:
            print(i)
            i.remove(ttp)
        else:
            continue

if count_ttp == len(ttp_list):
    extracted_dict["TTP"] = ttp_list
else:
    print("Error: Not all TTPs were extracted.")

for actor in json_load:
    for i in json_load[actor]:
        count_actor += 1
        actor_list.append(actor)

if count_actor == len(actor_list):
    extracted_dict["Actor"] = actor_list
else:
    print("Error: Not all actors were extracted.")

df = pd.DataFrame.from_dict(extracted_dict)

# checking that there is no row mismatch and count is the same
if len(df) == count_report and len(df) == count_ttp and len(df) == count_actor:
    print("Dataframe created correctly with no missing data.")
else:
    print("Error: Dataframe not created correctly")

# getting the different types of TTP and counts for each TTP
def to_1D(series):
    return pd.Series([x for _list in series for x in _list])
print(to_1D(df["TTP"]).value_counts())
print(df.head())

df.to_csv(os.path.join("assets","ruscraper_results.csv"),index=False)