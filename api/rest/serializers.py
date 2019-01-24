from flask_restplus import fields, reqparse

from rest import api

trending_model = api.model('Trending Model', {
    'name': fields.String,
    'query': fields.String,
    'volume': fields.Integer(attribute='tweet_volume'),
})

tweet_model = api.model('Tweet Model', {
    'text': fields.String,
    'sentiment': fields.String,
    'attention': fields.List(fields.Float),
    'fullname': fields.String,
    'nickname': fields.String,
    'created': fields.String,
    'photo_url': fields.String,
})

custom_tweet_model = api.model('Custom Tweet Model', {
    'text': fields.String,
    'sentiment': fields.String,
    'attention': fields.List(fields.Float),
})

tweets_query_parser = reqparse.RequestParser()
tweets_query_parser.add_argument('query', type=str, required=True)
tweets_query_parser.add_argument('size', type=int, required=True)

custom_tweet_query_parser = reqparse.RequestParser()
custom_tweet_query_parser.add_argument('content', type=str, required=True)
