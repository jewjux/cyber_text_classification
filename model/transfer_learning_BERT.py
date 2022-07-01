import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import transformers
from transformers import AutoModel, BertTokenizerFast
import pandas.plotting._matplotlib

df = pd.read_csv(os.path.join("assets","training.csv"))

encoded_dict = {
	'No technique found': 0,
	'Initial Access: T1078 Valid Accounts': 1,
	'Initial Access: T1091 Replication Through Removable Media': 2,
	'Initial Access: T1133 External Remote Services': 3,
	'Initial Access: T1189 Drive-by Compromise': 4,
    'Initial Access: T1190 Exploit Public-Facing Application':5,
    'Initial Access: T1199 Trusted Relationship':6,
	'Initial Access: T1566 Phishing': 7,
	'No technique found': 8
}

df['Technique'] = df.Technique.map(encoded_dict)
print(df.shape)

train_eg, temp_eg, train_techn, temp_techn = train_test_split(df['Example'], df['Technique'], random_state=2018, test_size=0.1, stratify=df['Technique'])

val_eg, test_eg, val_techn, test_techn = train_test_split(temp_eg, temp_techn, random_state=2018, test_size=0.5, stratify=temp_techn)

# import BERT-base pretrained model
bert = AutoModel.from_pretrained('bert-base-uncased')

# Load the BERT tokenizer
tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')

# get length of all the messages in the train set = 40

# tokenize and encode sequences in the training set
tokens_train = tokenizer.batch_encode_plus(
    train_eg.tolist(),
    max_length = 40,
    pad_to_max_length=True,
    truncation=True
)

# tokenize and encode sequences in the validation set
tokens_val = tokenizer.batch_encode_plus(
    val_eg.tolist(),
    max_length = 40,
    pad_to_max_length=True,
    truncation=True
)

# tokenize and encode sequences in the test set
tokens_test = tokenizer.batch_encode_plus(
    test_eg.tolist(),
    max_length = 40,
    pad_to_max_length=True,
    truncation=True
)

## convert lists to tensors

train_seq = torch.tensor(tokens_train['input_ids'])
train_mask = torch.tensor(tokens_train['attention_mask'])
train_y = torch.tensor(train_techn.tolist())

val_seq = torch.tensor(tokens_val['input_ids'])
val_mask = torch.tensor(tokens_val['attention_mask'])
val_y = torch.tensor(val_techn.tolist())

test_seq = torch.tensor(tokens_test['input_ids'])
test_mask = torch.tensor(tokens_test['attention_mask'])
test_y = torch.tensor(test_techn.tolist())

from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler

#define a batch size
batch_size = 32

# wrap tensors
train_data = TensorDataset(train_seq, train_mask, train_y)

# sampler for sampling the data during training
train_sampler = RandomSampler(train_data)

# dataLoader for train set
train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=batch_size)

# wrap tensors
val_data = TensorDataset(val_seq, val_mask, val_y)

# sampler for sampling the data during training
val_sampler = SequentialSampler(val_data)

# dataLoader for validation set
val_dataloader = DataLoader(val_data, sampler = val_sampler, batch_size=batch_size)