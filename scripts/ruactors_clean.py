# Cleaning the data for the same format as the general training data

import os
import re
import json
import pandas as pd

df = pd.read_csv(os.path.join("assets","ruscraper_results.csv"))

# matching the ttp provided to MITRE ATT&CK TTP
'''
Defacement -> Impact/Defacement
Exploit Development -> Resource Development/Develop Capabilities
Hardware_Supply Chain Compromise -> Initial Access/Supply Chain Compromise
Web Application Attacks -> Initial Access/Exploit Public-Facing Application
Domain Registration_DNS Abuse and Manipulation -> Initial Access/Valid Accounts
Domain Registration/DNS Abuse and Manipulation -> Initial Access/Valid Accounts
'''

# make TTP rows into list
df["TTP"] = df["TTP"].apply(eval)

# creating new df with the initial access data
matches = []
matches_ttp = []

for n, i in enumerate(df["TTP"]):
    for ttp in i:
        if ttp == "Hardware_Supply Chain Compromise" or ttp == "Domain Registration_DNS Abuse and Manipulation" or ttp == "Domain Registration/DNS Abuse and Manipulation" or ttp == "Web Application Attacks":
            matches.append(n)
            matches_ttp.append(ttp)

for i in range(len(matches_ttp)):
    if matches_ttp[i] == "Hardware_Supply Chain Compromise":
        matches_ttp[i] = "Initial Access: T1195 Supply Chain Compromise"
    elif matches_ttp[i] == "Domain Registration_DNS Abuse and Manipulation" or matches_ttp[i] == "Domain Registration/DNS Abuse and Manipulation":
        matches_ttp[i] = "Initial Access: T1078 Valid Accounts"
    elif matches_ttp[i] == "Web Application Attacks":
        matches_ttp[i] = "Initial Access: T1190 Exploit Public-Facing Application"

matches_reports = []
for i in matches:
    matches_reports.append(df.iloc[i,0])

# matches_actor = []
# for i in matches:
#     matches_actor.append(df.iloc[i,2])

matches_dict = {}
matches_dict["Technique"] = matches_ttp
matches_dict["Reports"] = matches_reports
# matches_dict["Actor"] = matches_actor

df_extracted = pd.DataFrame.from_dict(matches_dict)
print(df_extracted.head())

df_extracted.to_csv(os.path.join("assets","ru_initialaccess.csv"),index=False)

# analysing duplicates
# count_dict = {}
# for i in matches:
#     if i not in count_dict:
#         count_dict[i] = 0
#     if i in count_dict:
#         count_dict[i] += 1

# duplicates = [k for k,v in count_dict.items() if v>1]

# duplicated_reports = [df.iloc[i,0] for i in duplicates]

# for i in duplicated_reports:
#     print(len(i.split(" ")))