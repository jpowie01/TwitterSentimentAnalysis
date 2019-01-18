import pickle

from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

from utils import clean_text

LONGEST_SEQUENCE = 50

with open('./model_data/tokenizer.pickle', 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)

model = load_model('./model_data/weights.h5')


def analyse_sentiment(text):
    texts = [clean_text(text)]
    sequences = tokenizer.texts_to_sequences(texts)
    sequences = pad_sequences(sequences, maxlen=LONGEST_SEQUENCE)
    output = model.predict(sequences)
    print(output)

