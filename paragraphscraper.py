import pandas as pd 
import json
import pickle

df = pd.read_json('annotations_20220531.json', encoding_errors='ignore')

examples_list = []
generated_techniques_dict = {}

collated_dict = {}

# {'0': [Example, Technique], '1'; [example, [list of techniques]]}

for i in range(len(df)):
    if len(df.iloc[i,0]['_source']['paragraphs']) == 1:
        example_technique_list = []
        replaced = df.iloc[i,0]['_source']['paragraphs'][0].replace('\n', ' ')
        example_technique_list.append(replaced)
        generated_techniques_list = []
        for e in range(len(df.iloc[i,0]['_source']['spacyNER'])): # list
            if df.iloc[i,0]['_source']['spacyNER'][e]['label'] == 'MITRE_TTP':
                generated_techniques_list.append(df.iloc[i,0]['_source']['spacyNER'][e]['pretty_label'])
            else:
                continue
        example_technique_list.append(generated_techniques_list)
        collated_dict[i] = example_technique_list
    else:
        continue
        

df = pd.DataFrame.from_dict(collated_dict, orient='index', columns=['Example', 'Generated Techniques'])

with open('model_best.pkl', 'rb') as model:
     classifier = pickle.load(model)

def predict(example):
    technique = classifier.predict(example)
    return technique

df['Predicted Technique'] = predict(str(df.iloc[i,0]) for i in range(len(df)))

#df['Predicted Technique'] = df.apply(lambda x: predict(x['Example']), axis=1)

df['Match'] = 'False'

for i in range(len(df['Generated Techniques'])):
    if (df.iloc[i,2] == 'No technique found\t'): # error in training data have \t
        if len(df.iloc[i,1]) == 0:
            df.iloc[i,3] = 'True'
        else:
            for r in ["T1566","T1190", "T1078", "T1189", "T1133"]:
                if any(r in e for e in df.iloc[i,1]):
                    break
                elif not any(r in e for e in df.iloc[i,1]):
                    df.iloc[i,3] = 'True'
    else:
        for e in df.iloc[i,1]:
            if df.iloc[i,2].split(' ')[3] in e:
                df.iloc[i,3] = 'True'


df.to_csv('predicted.csv', index=False, encoding='utf-8')

print(df['Match'].value_counts())