import enum
import pickle
import string

import numpy as np
from keras import layers, models
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from scipy.ndimage.filters import gaussian_filter

from utils import clean_text


class Sentiment(enum.IntEnum):
    NEGATIVE = 0
    POSITIVE = 1
    NEUTRAL = 2


PATH_TO_WEIGHTS = './model_data/weights.h5'
PATH_TO_TOKENIZER = './model_data/tokenizer.pickle'

NEUTRAL_TRESHOLD = 0.6
LONGEST_SEQUENCE = 118
MAX_FEATURES = 5000
EMBEDDING_DIMENTION = 128
LSTM_OUTPUT = 256

ATTENTION_SCALE = 8

sentiment_model = None
attention_model = None

with open(PATH_TO_TOKENIZER, 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)


def convert_sentiments(sentiments):
    sentiments_with_neutral = np.zeros((sentiments.shape[0], 3))
    sentiments_with_neutral[:, 0:2] = sentiments
    sentiments_with_neutral[:, 2] = np.array(np.max(sentiments, axis=1) < NEUTRAL_TRESHOLD).astype(int)
    return [Sentiment(sentiment) for sentiment in np.argmax(sentiments_with_neutral, axis=1)]


def convert_attentions(texts, attentions):
    output = []
    for text, attention in zip(texts, attentions):
        number_of_words = len(text.split(' '))
        print(attention[:,0])
        attention = np.array(attention[-number_of_words:, 0])
        print(attention)
        #normalized_attention = attention / np.sum(attention)
        #print(normalized_attention)
        normalized_attention = attention * ATTENTION_SCALE
        print(normalized_attention)
        normalized_attention = np.clip(normalized_attention, 0, 1)
        print(normalized_attention)

        output.append(list(reversed(normalized_attention.tolist())))
    return output


def get_sentiment_model():
    global sentiment_model
    if sentiment_model is not None:
        return sentiment_model
    sentiment_model = load_model(PATH_TO_WEIGHTS)
    return sentiment_model


def get_attention_model():
    global attention_model
    if attention_model is not None:
        return attention_model

    sentiment_model = get_sentiment_model()

    model_input = layers.Input(shape=[LONGEST_SEQUENCE])
    embedding = layers.Embedding(MAX_FEATURES, EMBEDDING_DIMENTION, dropout=0.5,
                                 weights=sentiment_model.layers[1].get_weights())(model_input)
    lstm = layers.LSTM(LSTM_OUTPUT, dropout=0.5, recurrent_dropout=0.5, return_sequences=True,
                       weights=sentiment_model.layers[2].get_weights())(embedding)
    attention = layers.Dense(1, activation='tanh', weights=sentiment_model.layers[3].get_weights())(lstm)
    attention = layers.Flatten(weights=sentiment_model.layers[4].get_weights())(attention)
    attention = layers.Activation('softmax', weights=sentiment_model.layers[5].get_weights())(attention)
    attention = layers.RepeatVector(LSTM_OUTPUT, weights=sentiment_model.layers[6].get_weights())(attention)
    attention = layers.Permute([2, 1], weights=sentiment_model.layers[7].get_weights())(attention)
    attention_model = models.Model(inputs=[model_input], outputs=[attention])
    attention_model.compile(loss='categorical_crossentropy', optimizer='adam')
    return attention_model


def analyse_sentiment(texts):
    sentiment_model = get_sentiment_model()
    attention_model = get_attention_model()

    texts_without_punctations = []
    for text in texts:
        output = ''
        for word in text.split(' '):
            # Replace all standalone emojis with UNK token
            if all(character > '\uFFFF' for character in word):
                output += 'unk '
            # Replace all standalone punctations with UNK token
            elif all(character in string.punctuation for character in word):
                output += 'unk '
            # Otherwise, pass it to the network
            else:
                output += word + ' '

        # Make sure not to leave empty space at the end
        output = output[:-1] if output[-1] == ' ' else output
        texts_without_punctations.append(output)

    clean_texts = [clean_text(text) for text in texts_without_punctations]
    sequences = tokenizer.texts_to_sequences(clean_texts)
    padded_sequences = pad_sequences(sequences, maxlen=LONGEST_SEQUENCE)
    sentiments = sentiment_model.predict(padded_sequences)
    attentions = attention_model.predict(padded_sequences)
    return convert_sentiments(sentiments), convert_attentions(texts_without_punctations, attentions)
