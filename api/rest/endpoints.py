import urllib

import tweepy
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

import twitter
from rest import api, serializers

COUNTRY_TO_WOEID = {
    'UK': 23424975,
    'USA': 23424977,
}


@api.route('/trending/<string:country>')
class CurrentlyTrending(Resource):

    @api.marshal_list_with(serializers.trending_model)
    def get(self, country):
        woeid = COUNTRY_TO_WOEID.get(country.upper())
        if not woeid:
            raise BadRequest('This country is currently unsupported!')

        response = twitter.api.trends_place(woeid)
        trends = response[0]['trends']
        return sorted(trends, key=lambda trend: trend.get('tweet_volume', 0) or 0, reverse=True)


@api.route('/tweets')
class Tweets(Resource):

    @api.expect(serializers.tweets_query_parser)
    @api.marshal_list_with(serializers.tweet_model)
    def get(self):
        args = serializers.tweets_query_parser.parse_args()
        query = '"' + args.query + '"'
        query = urllib.parse.quote(query)
        tweets = tweepy.Cursor(twitter.api.search, q=query, lang='en', tweet_mode='extended').items(args.size)
        return list(tweets)