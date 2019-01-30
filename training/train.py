import os
import pickle
import multiprocessing

import numpy as np
import pandas as pd
import tensorflow as tf
from keras import models, layers, optimizers, regularizers, callbacks, backend as K
from sklearn.model_selection import train_test_split

# Choose between GPU and CPU implementation for LSTM
GPU_AVAILABLE = bool(K.tensorflow_backend._get_available_gpus())

# Configure TF for best performance
config = tf.ConfigProto(intra_op_parallelism_threads=multiprocessing.cpu_count(),
                        inter_op_parallelism_threads=multiprocessing.cpu_count(),
                        device_count = {'CPU' : 1, 'GPU' : 1 if GPU_AVAILABLE else 0})
session = tf.Session(config=config)
K.set_session(session)

# Load dataset from files
X = np.load('dataset/X.npy')
Y = np.load('dataset/Y.npy')

# Some hyperparameters for the model
MAX_FEATURES = 5000
EMBEDDING_DIMENTION = 128
LSTM_OUTPUT = 128

# ...and training
LEARNING_RATE = 0.001
BATCH_SIZE = 1024
EPOCHS = 50

# Prepare optimizer
adam = optimizers.Adam(lr=LEARNING_RATE, beta_1=0.9, beta_2=0.999)

# ...and the model
model_input = layers.Input(shape=[X.shape[1]])
embedding = layers.Embedding(MAX_FEATURES, EMBEDDING_DIMENTION, dropout=0.5)(model_input)
lstm = layers.LSTM(LSTM_OUTPUT, dropout=0.5, recurrent_dropout=0.5, return_sequences=True)(embedding)
attention = layers.Dense(1, activation='tanh')(lstm)
attention = layers.Flatten()(attention)
attention = layers.Activation('softmax')(attention)
attention = layers.RepeatVector(LSTM_OUTPUT)(attention)
attention = layers.Permute([2, 1])(attention)
representation = layers.multiply([lstm, attention])
representation = layers.Lambda(lambda xin: K.sum(xin, axis=-2), output_shape=(LSTM_OUTPUT,))(representation)
output = layers.Dense(2, activation='softmax', kernel_regularizer=regularizers.l2(0.0004),
                      activity_regularizer=regularizers.l1(0.0002))(representation)
model = models.Model(inputs=[model_input], outputs=[output])
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
print(model.summary())

# Split our dataset into training, validation and testing
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
X_validate, X_test, Y_validate, Y_test = train_test_split(X_test, Y_test, test_size=0.5, random_state=13)
print('Training dataset:', X_train.shape, 'x', Y_train.shape)
print('Validation dataset:', X_validate.shape, 'x', Y_validate.shape)
print('Testing dataset', X_test.shape, 'x', Y_test.shape)

# Do the "magic" ie. training!
os.makedirs('./output', exist_ok=True)
CHECKPOINT_NAME = './output/sentiment_analysis_weights.{epoch:02d}__{val_loss:.3f}__{val_acc:.3f}.h5'
model_checkpoint = callbacks.ModelCheckpoint(CHECKPOINT_NAME, verbose=1)
model.fit(X_train, Y_train, validation_data=(X_validate, Y_validate),
          epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1, callbacks=[model_checkpoint])

# Check for quality of the model on test data
loss, accuracy = model.evaluate(X_test, Y_test, batch_size=BATCH_SIZE, verbose=1)
print('Loss:', loss, 'Accuracy:', accuracy)
