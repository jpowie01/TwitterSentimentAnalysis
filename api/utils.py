import re
import string

import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

nltk.download('punkt', download_dir='./nltk/')
nltk.download('stopwords', download_dir='./nltk/')

stemmer = PorterStemmer()


def clean_text(text, remove_words=True):
    text = text.lower().replace('rt', '')
    text = "".join([ch for ch in text if ch not in string.punctuation])
    text = ' '.join(re.sub(r"(@[A-Za-z0-9]+( tweeted:)?)|([^0-9A-Za-z \t])|(https?\S*)|(\w+:\/\/\S+)"
                           , "UNK", text).split())
    tokens = nltk.word_tokenize(text)
    tokens = [word if word not in stopwords.words('english') else "UNK" for word in tokens]

    stems = [stemmer.stem(item) for item in tokens]
    return ' '.join(stems)
