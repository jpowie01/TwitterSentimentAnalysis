import enum
import pickle

import numpy as np
from keras import layers, models, backend as K
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

from utils import clean_text


class Sentiment(enum.IntEnum):
    NEGATIVE = 0
    POSITIVE = 1


LONGEST_SEQUENCE = 118
MAX_FEATURES = 5000
EMBEDDING_DIMENTION = 128
LSTM_OUTPUT = 256

sentiment_model = None
attention_model = None

with open('./model_data/tokenizer.pickle', 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)


def convert_sentiments(sentiments):
    return [Sentiment(sentiment) for sentiment in np.argmax(sentiments, axis=1)]


def convert_attentions(texts, attentions):
    output = []
    for text, attention in zip(texts, attentions):
        converted_attention = []
        clean_text_without_stopwords = clean_text(text).split(' ')
        clean_text_with_all_words = clean_text(text, remove_words=False).split(' ')
        j = 1
        for i, word in enumerate(reversed(clean_text_with_all_words), 1):
            if clean_text_with_all_words[-i] == clean_text_without_stopwords[-j]:
                converted_attention.append(attention[-i])
                j = min(j + 1, len(clean_text_without_stopwords))
            else:
                converted_attention.append(0.0)
        output.append(list(reversed(converted_attention)))
    return output


def get_sentiment_model():
    global sentiment_model
    if sentiment_model is not None:
        return sentiment_model
    sentiment_model = load_model('./model_data/weights.h5')
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
    representation = layers.multiply([lstm, attention])
    representation = layers.Lambda(lambda xin: K.sum(xin, axis=-2), output_shape=(LSTM_OUTPUT,))(representation)
    attention_model = models.Model(inputs=[model_input], outputs=[representation])
    attention_model.compile(loss='categorical_crossentropy', optimizer='adam')
    return attention_model


def analyse_sentiment(texts):
    sentiment_model = get_sentiment_model()
    attention_model = get_attention_model()

    clean_texts = [clean_text(text) for text in texts]
    sequences = tokenizer.texts_to_sequences(clean_texts)
    padded_sequences = pad_sequences(sequences, maxlen=LONGEST_SEQUENCE)
    sentiments = sentiment_model.predict(padded_sequences)
    attentions = attention_model.predict(padded_sequences)
    return convert_sentiments(sentiments), convert_attentions(texts, attentions)

