import urllib

import tweepy
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

import twitter
from rest import api, serializers
from sentiment_analysis import analyse_sentiment

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
        output = []
        for tweet in tweets:
            if 'retweeted_status' in dir(tweet):
                tweet_text = tweet.retweeted_status.full_text
            else:
                tweet_text = tweet.full_text

            sentiment, attention = analyse_sentiment([tweet_text])
            output.append({
                'text': tweet_text,
                'sentiment': sentiment[0].name,
                'attention': attention[0],
                'fullname': tweet.author.name,
                'nickname': tweet.author.screen_name,
                'created': tweet.created_at.isoformat(),
                'photo_url': tweet.author.profile_image_url,
            })
        return output
