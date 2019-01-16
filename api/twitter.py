import os

import tweepy


CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
assert CONSUMER_KEY and CONSUMER_SECRET, 'Remember to set up your CONSUMER_KEY and CONSUMER_SECRET!'

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
assert CONSUMER_KEY and CONSUMER_SECRET, 'Remember to set up your ACCESS_TOKEN and ACCESS_TOKEN_SECRET!'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

