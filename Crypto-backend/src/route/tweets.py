from src.HuggingFaceTransformersAnalysis import HuggingFaceTransformersAnalysis
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask import Blueprint, request
from flask.json import jsonify
from src.providers.TwitterData import TwitterData
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_cors import cross_origin
from src.database import Cryptocurrency, Tweet, db
from flasgger import swag_from
from sqlalchemy import desc, asc
from datetime import datetime, timedelta
from sqlalchemy import func

tweets = Blueprint("tweets", __name__, url_prefix="/api/v1/tweets")

@tweets.get('/upload')
def upload():
    cryptocurrencies = Cryptocurrency.query
    monitored_tickers = []
    for cryptocurrency in cryptocurrencies:
        monitored_tickers.append(cryptocurrency.abbreviation)
    #Twitter data : 
    data = TwitterData(monitored_tickers)
    tweetsData = data.getData()
    sentimentAnalysis = HuggingFaceTransformersAnalysis()
    for ticker in monitored_tickers:
        label = []
        cryptocurrency = Cryptocurrency.query.filter_by(abbreviation=ticker).first()
        for counter in range(len(tweetsData[ticker])):
            try:
                text = tweetsData[ticker][counter]
                score = sentimentAnalysis.sentiment(sentimentAnalysis.convertEmoji(tweetsData[ticker][counter]))
                label = score[0]['label']
                score = score[0]['score']
                if not Tweet.query.filter_by(text=text).first():
                    #tweet = Tweet(text=text, label=label, score=float(score), created_at=datetime(2022, 8, 9), cryptocurrency_id=cryptocurrency.id)
                    tweet = Tweet(text=text, label=label, score=float(score), cryptocurrency_id=cryptocurrency.id)
                    db.session.add(tweet)
                    db.session.commit()
            except IndexError:
                print('List index out of range')
    return jsonify({
        'response': 'tweets uploded .'
    }), HTTP_201_CREATED

@tweets.get('/')
@cross_origin(origin='localhost:4200',headers=['Content-Type','Authorization'])
def get_tweets_by_cryptocurrency():
    crypto = request.args.get('crypto', '', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 0, type=int)
    cryptocurrency = Cryptocurrency.query.filter_by(abbreviation=crypto).first()
    if(cryptocurrency):
        days = request.args.get('days', 31, type=int)
        if(per_page == 0 ) : 
            tweets = Tweet.query.order_by(desc(Tweet.created_at)).filter_by(cryptocurrency_id=cryptocurrency.id).filter(func.date(Tweet.created_at) >= (datetime.today() - timedelta(days=days))).filter(func.date(Tweet.created_at) <= (datetime.today()))
        else:
            tweets = Tweet.query.order_by(desc(Tweet.created_at)).filter_by(cryptocurrency_id=cryptocurrency.id).filter(func.date(Tweet.created_at) >= (datetime.today() - timedelta(days=days))).filter(func.date(Tweet.created_at) <= (datetime.today()))
            meta = {
                "page": tweets.page,
                'pages': tweets.pages,
                'total_count': tweets.total,
                'prev_page': tweets.prev_num,
                'next_page': tweets.next_num,
                'has_next': tweets.has_next,
                'has_prev': tweets.has_prev
            }
        data = []
        for tweet in tweets:
            data.append({
                'id': tweet.id,
                'text': tweet.text,
                'label': tweet.label,
                'score': tweet.score,
                'created_at': tweet.created_at,
                'cryptocurrency': tweet.cryptocurrency.abbreviation
            })
        if(per_page == 0 ) : 
            meta = {
                "page": 1,
                'pages': 1,
                'total_count': len(data),
                'prev_page': 0,
                'next_page': 1,
                'has_next': False,
                'has_prev': False
            }
        res = jsonify({'data': data, 'meta': meta}), HTTP_200_OK
        return res
    return jsonify({
        'response': 'the cryptocurrency does not exist ! ! !'
    }), HTTP_404_NOT_FOUND


