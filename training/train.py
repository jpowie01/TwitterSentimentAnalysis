import os
import pickle

import numpy as np
import pandas as pd
from keras import regularizers
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM
from sklearn.model_selection import train_test_split

from attention import AttentionLayer

# Load dataset from files
X = np.load('dataset/X.npy')
Y = np.load('dataset/Y.npy')

# Some hyperparameters for the model
MAX_FEATURES = 5000
EMBEDDING_DIMENTION = 128
LSTM_OUTPUT = 256

# ...and prepare this model
model = Sequential()
model.add(Embedding(MAX_FEATURES, EMBEDDING_DIMENTION, input_length = X.shape[1], dropout=0.2))
model.add(LSTM(LSTM_OUTPUT, dropout_U=0.2, dropout_W=0.2, kernel_regularizer=regularizers.l2(0.0004),
               activity_regularizer=regularizers.l1(0.0002), return_sequences=True))
model.add(AttentionLayer())
model.add(Dense(2, activation='softmax', kernel_regularizer=regularizers.l2(0.0004),
                activity_regularizer=regularizers.l1(0.0002)))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
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
