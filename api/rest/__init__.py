from flask import Blueprint
from flask_restplus import Api


blueprint = Blueprint('api', __name__)
api = Api(blueprint, version='1.0', title='Twitter Sentiment Analysis API',
          description='Documentation for Twitter Sentiment Analysis API.')

