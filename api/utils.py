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
                           , "", text).split())
    tokens = nltk.word_tokenize(text)
    if remove_words:
        tokens = [word for word in tokens if word not in stopwords.words('english')]

    stems = [stemmer.stem(item) for item in tokens]
    return ' '.join(stems)
