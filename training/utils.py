import re
import string

import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords


nltk.download('punkt', download_dir='./nltk/')
nltk.download('stopwords', download_dir='./nltk/')


stemmer = PorterStemmer()
def clean_text(text):
    text = text.lower()
    text = text.replace('rt', '')
    text = ''.join(character for character in text if character not in string.punctuation)
    text = ''.join(character for character in text if character <= '\uFFFF')  # Remove all emojis
    text = ' '.join(re.sub(r'(@[A-Za-z0-9]+( tweeted:)?)|([^0-9A-Za-z \t])|(https?\S*)|(\w+:\/\/\S+)',
                           'unk', text).split())  # Remove all garbage
    tokens = nltk.word_tokenize(text)
    tokens = [word if word not in stopwords.words('english') else 'unk' for word in tokens]
    stems = [stemmer.stem(item) for item in tokens]
    return ' '.join(stems)
