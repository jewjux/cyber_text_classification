# for model
import tensorflow as tf
from tensorflow import keras
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from keras.initializers import TruncatedNormal
from keras.losses import CategoricalCrossentropy
from keras.metrics import CategoricalAccuracy
from keras.utils import to_categorical
from keras.layers import Input, Dense

#https://www.kaggle.com/code/thebrownviking20/bert-multiclass-classification/notebook
#https://www.analyticsvidhya.com/blog/2021/12/multiclass-classification-using-transformers/
#https://www.analyticsvidhya.com/blog/2021/12/manual-for-the-first-time-users-google-bert-for-text-classification/
#https://gist.github.com/analyticsindiamagazine/97f53c3a6ee5f63efea92e4159792f92#file-predicting_news_category_with_bert_in_tensorflow-ipynb
#https://towardsdatascience.com/building-a-multi-label-text-classifier-using-bert-and-tensorflow-f188e0ecdc5d
#https://analyticsindiamag.com/step-by-step-guide-to-implement-multi-class-classification-with-bert-tensorflow/
#https://towardsdatascience.com/multi-class-text-classification-with-deep-learning-using-bert-b59ca2f5c613
#https://colab.research.google.com/github/huggingface/notebooks/blob/master/examples/text_classification.ipynb
#https://github.com/Dirkster99/PyNotes/blob/master/Transformers/LocalModelUsage_Finetuning/30%20MultiClass%20Classification%20in%2010%20Minutes%20with%20BERT-TensorFlow-SoftMax-LocalModel.ipynb
#https://colab.research.google.com/drive/18vy67le2DC-iMJK-AiB0vVKtMRAxmBnB?usp=sharing