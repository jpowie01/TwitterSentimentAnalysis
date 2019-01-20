import enum
import pickle

import numpy as np
from keras import layers, models, backend as K
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from scipy.ndimage.filters import gaussian_filter

from utils import clean_text


# NOTE: This will be remove in the next PR as new models are trained without F1 Measure
def f1_measure(y_true, y_pred):
    def recall(y_true, y_pred):
        """Recall metric.

        Only computes a batch-wise average of recall.

        Computes the recall, a metric for multi-label classification of
        how many relevant items are selected.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    def precision(y_true, y_pred):
        """Precision metric.

        Only computes a batch-wise average of precision.

        Computes the precision, a metric for multi-label classification of
        how many selected items are relevant.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision
    precision = precision(y_true, y_pred)
    recall = recall(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))


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
        converted_attention = []

        # We need two versions of our text:
        #  - without stopwords, which was passed to the neural network
        #  - with all the words, which we will be comparing to in order to map attention to original text
        clean_text_without_stopwords = clean_text(text).split(' ')
        clean_text_with_all_words = clean_text(text, remove_words=False).split(' ')

        # Iterate from the back and match each words. If equal - we found attention value for given original word
        j = 1
        for i, word in enumerate(reversed(clean_text_with_all_words), 1):
            if clean_text_with_all_words[-i] == clean_text_without_stopwords[-j]:
                converted_attention.append(attention[-i,0])
                j = min(j + 1, len(clean_text_without_stopwords))
            else:
                converted_attention.append(0.0)

        # Fill all the zeros with values from Gaussian filter
        converted_attention = np.array(converted_attention)
        smoothed_attention = gaussian_filter(converted_attention, 1.0)
        converted_attention[converted_attention == 0] = smoothed_attention[converted_attention == 0]

        output.append(list(reversed(converted_attention.tolist())))
    return output


def get_sentiment_model():
    global sentiment_model
    if sentiment_model is not None:
        return sentiment_model
    sentiment_model = load_model(PATH_TO_WEIGHTS, custom_objects={'f1_measure': f1_measure})
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

    clean_texts = [clean_text(text) for text in texts]
    sequences = tokenizer.texts_to_sequences(clean_texts)
    padded_sequences = pad_sequences(sequences, maxlen=LONGEST_SEQUENCE)
    sentiments = sentiment_model.predict(padded_sequences)
    attentions = attention_model.predict(padded_sequences)
    return convert_sentiments(sentiments), convert_attentions(texts, attentions)

