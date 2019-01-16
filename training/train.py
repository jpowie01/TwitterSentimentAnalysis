import os
import re
import pickle
import string

import nltk
import pandas as pd
from keras import regularizers
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

from attention import AttentionWithContext


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
dataset = dataset[:30000]  # TODO: REMOVE ME !

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

# Some hyperparameters for the model
EMBEDDING_DIMENTION = 128
LSTM_OUTPUT = 256

# ...and prepare this model
model = Sequential()
model.add(Embedding(MAX_FEATURES, EMBEDDING_DIMENTION, input_length = X.shape[1], dropout=0.2))
model.add(LSTM(LSTM_OUTPUT, dropout_U=0.2, dropout_W=0.2, kernel_regularizer=regularizers.l2(0.0004),
               activity_regularizer=regularizers.l1(0.0002), return_sequences=True))
model.add(AttentionWithContext())
model.add(Dense(2, activation='softmax', kernel_regularizer=regularizers.l2(0.0004),
                activity_regularizer=regularizers.l1(0.0002)))
model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
print(model.summary())

# Split our dataset into training, validation and testing
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
X_validate, X_test, Y_validate, Y_test = train_test_split(X_test, Y_test, test_size=0.8, random_state=13)
print('Training dataset:', X_train.shape, 'x', Y_train.shape)
print('Validation dataset:', X_validate.shape, 'x', Y_validate.shape)
print('Testing dataset', X_test.shape, 'x', Y_test.shape)

# Do the "magic" ie. training!
BATCH_SIZE = 100
EPOCHS = 20
model.fit(X_train, Y_train, validation_data=(X_validate, Y_validate),
          epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=2)

# Save the model, so that we will be able to use it in our application
os.makedirs('./output', exist_ok=True)
model.save('./output/sentiment_analysis_model.h5')

# Also, save the tokenizer, so that we will be able to use the same one in out application
with open('./output/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
