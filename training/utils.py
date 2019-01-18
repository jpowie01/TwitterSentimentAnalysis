import re
import string

import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords


nltk.download('punkt', download_dir='./nltk/')
nltk.download('stopwords', download_dir='./nltk/')


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
