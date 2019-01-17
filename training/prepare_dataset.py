import re
import string

import nltk
import numpy as np
import pandas as pd

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.utils import shuffle
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

nltk.download('punkt', download_dir='./nltk/')
nltk.download('stopwords', download_dir='./nltk/')

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

# TODO: REFACTOR THIS METHOD FROM HERE
stemmer = PorterStemmer()
num = 0
def clean_text(text):
    text = text.lower().replace('rt', '')
    text = "".join([ch for ch in text if ch not in string.punctuation])
    text = ' '.join(re.sub(r"(@[A-Za-z0-9]+( tweeted:)?)|([^0-9A-Za-z \t])|(https?\S*)|(\w+:\/\/\S+)"
                           , "", text).split())
    tokens = nltk.word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]

    stems = [stemmer.stem(item) for item in tokens]
    global num
    num += 1
    if num % 30000 == 0:
        print(num)
    return ' '.join(stems)
# TODO: REFACTOR ENDS HERE

# Apply stemmer on all Tweets
dataset['text'] = dataset['Text'].apply(clean_text)

# Tokenize all Tweets, so that it'll be easier to understand them
MAX_FEATURES = 5000
print('Tokenizing...')
tokenizer = Tokenizer(num_words=MAX_FEATURES, split=' ')
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
