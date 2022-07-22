# 2: Padding Scraper
# Extracting examples for the specific tactic from EY data and padding it to training.csv
# Not able to scale to sub-techniques yet, only used to extract techniques.
# There are some difference in formatting of the padded data for sub-techniques so will have to separately add in more code if doing sub-techn

import csv
import os

# input tactic you want here
tactic = "Initial Access"

# get additional tactic data
padding_data_dict = {}

with open(os.path.join("assets","padding_data.tsv"), encoding="utf8", newline='') as file:
    tsv = csv.reader(file, delimiter="\t")
    for row in tsv:
        if row[4] == tactic: # only get tactic
            if "." not in row[3]: # making sure no sub techniques are added
                key = tactic + ": " + row[3].strip() + " " + row[2].strip() # getting the key name for dict
                if key in padding_data_dict:
                    #if not isinstance(padding_data_dict[key], list):
                        #padding_data_dict[key] = [padding_data_dict[key]]
                    padding_data_dict[key].append(row[1])
                else:
                    padding_data_dict[key] = [row[1]]
# padding_data_dict = {Tactic: Technique: }

# adding the additional padding data without filtering
with open(os.path.join("assets","training.csv"), 'a', encoding="utf8", newline='') as csvfile:
    headings = ['Technique', 'Example']
    new_val = csv.DictWriter(csvfile, fieldnames=headings)

    for k,v in padding_data_dict.items():
        if isinstance(padding_data_dict[key], list):
            for i in v:
                new_val.writerow({'Technique': k, 'Example': i})
        else:
            new_val.writerow({'Technique': k, 'Example': i})

# removing the duplicates and adding "." to make consistent sentences
writing_to_csv = [] # list will be [[Techniques, Example], [tech, eg.]]
with open(os.path.join("assets","training.csv"), 'r', encoding="utf8", newline='') as csvfile:
    for a in csv.reader(csvfile): # a is a list [tech, example]
        if a[1] != "Example":
            if a[1].replace(".","").strip() not in (i[1].replace(".","").strip() for i in writing_to_csv):
                a[1] = a[1].strip().rstrip(".")
                a[1] = a[1] + "."
                if "\n" in a[1]:
                    a[1] = a[1].replace("\n","")
                writing_to_csv.append(a)
            else:
                continue
        else:
            writing_to_csv.append(a) # adding [Technique, Example] heading

with open(os.path.join("assets","training.csv"), 'w', encoding="utf8", newline='') as csvfile:
    csv.writer(csvfile).writerows(writing_to_csv)

# removing techniques with less than 5 examples
num_of_examples = {}  # {Technique: No. of examples}
masterlist = []  # [[tech,example], [tech,example]]
removed_techniques = []
with open(os.path.join("assets","training.csv"), 'r', encoding="utf8", newline='') as csvfile:
    # Counter for number of examples per technique
    for a in csv.reader(csvfile): # a is a list [tech, example]
        masterlist.append(a)
        if a[0] not in num_of_examples:
            num_of_examples[a[0]] = 1
        if a[0] in num_of_examples:
            num_of_examples[a[0]] += 1
    # Removing techniques with </= 5 examples
    for k,v in num_of_examples.items():
        if (v <= 5) and (k != "Technique"):
            removed_techniques.append(k)
    for k in removed_techniques:
        for i in masterlist[:]: # Returning the entire list as when using .remove it will skip to the following value after removing
            if i[0] in k:
                masterlist.remove(i)
    print(f"Removed {', '.join(removed_techniques)} techniques due to limited examples found.")

with open(os.path.join("assets","training.csv"), 'w', encoding="utf8", newline='') as csvfile:
    csv.writer(csvfile).writerows(masterlist)
            
# adding the "No techniques found" data into training.csv
with open(os.path.join("assets","training.csv"), 'a', encoding="utf8", newline='') as final:
    with open(os.path.join("assets","training_no_techn.csv"), 'r', encoding='utf8', newline='') as raw:
        rows_to_add = [rows for rows in csv.reader(raw)]
    csv.writer(final).writerows(rows_to_add)

print("Padding completed.")
