# for model
import os
import numpy as np
import pandas as pd
import transformers
import tensorflow as tf
from tensorflow import keras
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from keras.initializers import TruncatedNormal
from keras.losses import CategoricalCrossentropy
from keras.metrics import CategoricalAccuracy
from keras.utils import to_categorical
from keras.layers import Input, Dense
from transformers import AutoTokenizer,TFBertModel
from sklearn.metrics import classification_report

df = pd.read_csv(os.path.join("assets","training.csv"))
'''
# Shuffle your dataset 
shuffle_df = df.sample(frac=1)

# Define a size for your train set 
train_size = int(0.8 * len(df))
validate_size = 0.5(len(df)-train_size)+train_size

# Split your dataset 
train_set = shuffle_df[:train_size]
test_set = shuffle_df[train_size:validate_size]
validate_set = shuffle_df[validate_size:]
'''
# Shuffle your dataset 
shuffle_df = df.sample(frac=1)

# Define a size for your train set 
train_size = int(0.7 * len(df))

# Split your dataset 
df_train = shuffle_df[:train_size]
df_test = shuffle_df[train_size:]
pd.options.mode.chained_assignment = None

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

df_train['Technique'] = df_train.Technique.map(encoded_dict)
df_test['Technique'] = df_test.Technique.map(encoded_dict)

y_train = to_categorical(df_train.Technique)
y_test = to_categorical(df_test.Technique)

tokeniser = AutoTokenizer.from_pretrained('bert-base-cased')
bert = TFBertModel.from_pretrained('bert-base-cased')

# Tokenise the input

x_train = tokeniser(
    text=df_train.Example.tolist(),
    add_special_tokens=True,
    max_length=70,
    truncation=True,
    padding=True, 
    return_tensors='tf',
    return_token_type_ids = False,
    return_attention_mask = True,
    verbose = True)
x_test = tokeniser(
    text=df_test.Example.tolist(),
    add_special_tokens=True,
    max_length=70,
    truncation=True,
    padding=True, 
    return_tensors='tf',
    return_token_type_ids = False,
    return_attention_mask = True,
    verbose = True)

input_ids = x_train['input_ids']
attention_mask = x_train['attention_mask']

max_len = 70
input_ids = Input(shape=(max_len,), dtype=tf.int32, name="input_ids")
input_mask = Input(shape=(max_len,), dtype=tf.int32, name="attention_mask")
embeddings = bert(input_ids,attention_mask = input_mask)[0] 
out = tf.keras.layers.GlobalMaxPool1D()(embeddings)
out = Dense(128, activation='relu')(out)
out = tf.keras.layers.Dropout(0.1)(out)
out = Dense(32,activation = 'relu')(out)
y = Dense(6,activation = 'sigmoid')(out)
model = tf.keras.Model(inputs=[input_ids, input_mask], outputs=y)
model.layers[2].trainable = True

optimizer = Adam(
    learning_rate=5e-05, # this learning rate is for bert model , taken from huggingface website 
    epsilon=1e-08,
    decay=0.01,
    clipnorm=1.0)
# Set loss and metrics
loss =CategoricalCrossentropy(from_logits = True)
metric = CategoricalAccuracy('balanced_accuracy'),
# Compile the model
model.compile(
    optimizer = optimizer,
    loss = loss, 
    metrics = metric)

train_history = model.fit(
    x ={'input_ids':x_train['input_ids'],'attention_mask':x_train['attention_mask']} ,
    y = y_train,
    validation_data = (
    {'input_ids':x_test['input_ids'],'attention_mask':x_test['attention_mask']}, y_test
    ),
  epochs=1,
    batch_size=36
)

predicted_raw = model.predict({'input_ids':x_test['input_ids'],'attention_mask':x_test['attention_mask']})

y_predicted = np.argmax(predicted_raw, axis = 1)
y_true = df_test.Technique

print(classification_report(y_true, y_predicted))