import pickle

import numpy as np
import pandas as pd

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.utils import shuffle

from utils import clean_text


# Read an annotate dataset with headers
print('Reading dataset...')
dataset = pd.read_csv('dataset/training.1600000.processed.noemoticon.csv', encoding='ISO-8859-1')
dataset.columns = ['Sentiment', 'ID', 'Date', 'Query', 'User', 'Text']
dataset = dataset.drop(['ID', 'Date', 'Query', 'User'], axis=1)

# Preprocess the dataset to remove neutral values and use 0s and 1s for negative and positive sentiment
print('Preprocessing...')
dataset = shuffle(dataset)
dataset = dataset[dataset['Sentiment'] != 2]
dataset['Sentiment'] = dataset['Sentiment'] / 4
dataset = dataset[:30]

# Apply stemmer on all Tweets
dataset['text'] = dataset['Text'].apply(clean_text)

# Tokenize all Tweets, so that it'll be easier to understand them
MAX_FEATURES = 5000
print('Tokenizing...')
tokenizer = Tokenizer(num_words=MAX_FEATURES, split=' ', oov_token='UNK')
tokenizer.fit_on_texts(dataset['Text'].values)

# Prepare dataset for training our LSTM
X = tokenizer.texts_to_sequences(dataset['Text'].values)
X = pad_sequences(X)
Y = pd.get_dummies(dataset['Sentiment']).values

# Save this dataset on the disk
np.save('dataset/X.npy', X)
np.save('dataset/Y.npy', Y)

# Also, save the tokenizer, so that we will be able to use the same one in out application
with open('./output/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
