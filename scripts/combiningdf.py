# For the ru actors + general training data

import os
import re
import json
import pandas as pd

df1 = pd.read_csv(os.path.join("assets","ru_initialaccess.csv"))
df2 = pd.read_csv(os.path.join("assets","training.csv"))

techniques_list = [df1.iloc[i,0] for i in range(len(df1))]
for i in range(len(df2)):
    techniques_list.append(df2.iloc[i,0])

example_list = [df1.iloc[i,1] for i in range(len(df1))]
for i in range(len(df2)):
    example_list.append(df2.iloc[i,1])

all_dict = {}
all_dict["Technique"] = techniques_list
all_dict["Example"] = example_list

df = pd.DataFrame.from_dict(all_dict)
print(df.head())
print(df["Technique"].value_counts())

df.to_csv(os.path.join("assets","collated.csv"),index=False)