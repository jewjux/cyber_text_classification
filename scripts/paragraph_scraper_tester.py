# 3: Paragraph Scraper and Tester
# Extracting the paragraphs (unseen data) and predicting on them
# Possible improvement is to make it more reusable (the comparing portion)

import pandas as pd
import pickle
import os

df = pd.read_json(os.path.join("assets","annotations_20220531.json"), encoding_errors='ignore')

examples_list = []
generated_techniques_dict = {}
collated_dict = {}

# extracting the examples (paragraphs) and generated techniques from dataset
for i in range(len(df)):
    if len(df.iloc[i,0]['_source']['paragraphs']) == 1:
        example_technique_list = []
        replaced = df.iloc[i,0]['_source']['paragraphs'][0].replace('\n', ' ')
        example_technique_list.append(replaced)
        generated_techniques_list = []
        for e in range(len(df.iloc[i,0]['_source']['spacyNER'])): # e is list of generated techniques in the dataset
            if df.iloc[i,0]['_source']['spacyNER'][e]['label'] == 'MITRE_TTP':
                generated_techniques_list.append(df.iloc[i,0]['_source']['spacyNER'][e]['pretty_label'])
            else:
                continue
        example_technique_list.append(generated_techniques_list)
        collated_dict[i] = example_technique_list
    else:
        continue
# collated dict is {'0': [Example, Technique], '1'; [example, [list of generated techniques]]}

df = pd.DataFrame.from_dict(collated_dict, orient='index', columns=['Example', 'Generated Techniques'])

with open(os.path.join("model","model_naivebayes.pkl"), 'rb') as model:
     classifier = pickle.load(model)

def predict(example):
    technique = classifier.predict(example)
    return technique

df['Predicted Technique'] = predict(str(df.iloc[i,0]) for i in range(len(df)))

# checking if the predicted is the same as the generated techniques (not that reusable)
df['Match'] = 'False'

print(df['Predicted Technique'].value_counts())

for i in range(len(df['Generated Techniques'])):
    if (df.iloc[i,2] == 'No technique found'):
        if len(df.iloc[i,1]) == 0:
            # empty generated technique
            df.iloc[i,3] = 'True'
        else:
            for r in ["T1566","T1190", "T1189", "T1078", "T1189", "T1133", "T1199", "T1091"]: # have to manually input the techn numbers that dataset was trained to
                if any(r in e for e in df.iloc[i,1]):
                    # will remain as False if there are any
                    break
                elif not any(r in e for e in df.iloc[i,1]):
                    df.iloc[i,3] = 'True'
    else:
        for e in df.iloc[i,1]:
            if df.iloc[i,2].split(' ')[2] in e:
                df.iloc[i,3] = 'True'

df.to_csv(os.path.join("assets","predicted.csv"), index=False, encoding='utf-8')

print(df['Match'].value_counts())