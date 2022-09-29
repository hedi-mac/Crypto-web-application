from src.HuggingFaceTransformersAnalysis import HuggingFaceTransformersAnalysis
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask import Blueprint, request
from flask.json import jsonify
from src.providers.TwitterData import TwitterData
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_cors import cross_origin
from src.database import Article, Cryptocurrency, Tweet, db
from flasgger import swag_from
from datetime import datetime, timedelta
from sqlalchemy import func

reviews = Blueprint("reviews", __name__, url_prefix="/api/v1/reviews")

@reviews.get('/pie-stats/<string:crypto>')
@cross_origin(origin='localhost:4200',headers=['Content-Type','Authorization'])
def get_pie_stats_by_cryptocurrency(crypto):
    cryptocurrency = Cryptocurrency.query.filter_by(abbreviation=crypto).first()
    if(cryptocurrency):
        days = request.args.get('days', 7, type=int)
        positive_articles = Article.query.filter_by(cryptocurrency_id=cryptocurrency.id, label='POSITIVE').filter(func.date(Article.created_at) >= (datetime.today() - timedelta(days=days))).filter(func.date(Article.created_at) <= (datetime.today())).count()
        positive_tweets = Tweet.query.filter_by(cryptocurrency_id=cryptocurrency.id, label='POSITIVE').filter(func.date(Tweet.created_at) >= (datetime.today() - timedelta(days=days))).filter(func.date(Tweet.created_at) <= (datetime.today())).count()
        positives = positive_articles + positive_tweets
        negative_articles = Article.query.filter_by(cryptocurrency_id=cryptocurrency.id, label='NEGATIVE').filter(func.date(Article.created_at) >= (datetime.today() - timedelta(days=days))).filter(func.date(Article.created_at) <= (datetime.today())).count()
        negative_tweets = Tweet.query.filter_by(cryptocurrency_id=cryptocurrency.id, label='NEGATIVE').filter(func.date(Tweet.created_at) >= (datetime.today() - timedelta(days=days))).filter(func.date(Tweet.created_at) <= (datetime.today())).count()
        negatives = negative_articles + negative_tweets 
        data = []
        data.append({
            'name': 'Positives',
            'selected': True,
            'sliced': True,
            'y': positives
        })
        data.append({
            'name': 'Negatives',
            'selected': False,
            'sliced': False,
            'y': negatives
        })
        return jsonify({
            'data': data
        }), HTTP_200_OK
    return jsonify({
        'response': 'the cryptocurrency does not exist ! ! !'
    }), HTTP_404_NOT_FOUND

@reviews.get('/bar-stats')
@cross_origin(origin='localhost:4200',headers=['Content-Type','Authorization'])
def get_bar_stats():
    cryptocurrencies = Cryptocurrency.query
    if(cryptocurrencies):
        days = request.args.get('days', 7, type=int)
        positives_list = []
        negatives_list = []
        for crypto in cryptocurrencies:
            cryptocurrency = Cryptocurrency.query.filter_by(abbreviation=crypto.abbreviation).first()
            positive_articles = Article.query.filter_by(cryptocurrency_id=cryptocurrency.id, label='POSITIVE').filter(func.date(Article.created_at) >= (datetime.today() - timedelta(days=days))).filter(func.date(Article.created_at) <= (datetime.today())).count()
            positive_tweets = Tweet.query.filter_by(cryptocurrency_id=cryptocurrency.id, label='POSITIVE').filter(func.date(Tweet.created_at) >= (datetime.today() - timedelta(days=days))).filter(func.date(Tweet.created_at) <= (datetime.today())).count()
            positives = positive_articles + positive_tweets
            positives_list.append(positives)
            negative_articles = Article.query.filter_by(cryptocurrency_id=cryptocurrency.id, label='NEGATIVE').filter(func.date(Article.created_at) >= (datetime.today() - timedelta(days=days))).filter(func.date(Article.created_at) <= (datetime.today())).count()
            negative_tweets = Tweet.query.filter_by(cryptocurrency_id=cryptocurrency.id, label='NEGATIVE').filter(func.date(Tweet.created_at) >= (datetime.today() - timedelta(days=days))).filter(func.date(Tweet.created_at) <= (datetime.today())).count()
            negatives = negative_articles + negative_tweets 
            negatives_list.append(negatives)
            data = []
        data.append({
                'positives': positives_list,
                'negatives': negatives_list
        }) 
        return jsonify({
                'data': data
            }), HTTP_200_OK
    return jsonify({
        'response': 'no cryptocurrencies ! ! !'
    }), HTTP_404_NOT_FOUND

@reviews.get('/evolution-stats')
@cross_origin(origin='localhost:4200',headers=['Content-Type','Authorization'])
def get_evolution_stats():
    cryptocurrencies = Cryptocurrency.query
    if(cryptocurrencies):
        tab = []
        days = request.args.get('days', 7, type=int)
        for crypto in cryptocurrencies:
            cryptocurrency = Cryptocurrency.query.filter_by(abbreviation=crypto.abbreviation).first()
            res = []
            rType = request.args.get('type', 'all', type=str)
            for i in range(0, days):
                d = i
                if(rType == 'all'): 
                    positive_tweets = Tweet.query.filter_by(cryptocurrency_id=cryptocurrency.id, label='POSITIVE').filter(func.date(Tweet.created_at) >= (datetime.today() - timedelta(days=d+1))).filter(func.date(Tweet.created_at) < (datetime.today() - timedelta(days=d))).count()
                    positive_articles = Article.query.filter_by(cryptocurrency_id=cryptocurrency.id, label='POSITIVE').filter(func.date(Article.created_at) >= (datetime.today() - timedelta(days=d+1))).filter(func.date(Article.created_at) < (datetime.today() - timedelta(days=d))).count()
                    pos = positive_tweets+positive_articles
                    negative_tweets = Tweet.query.filter_by(cryptocurrency_id=cryptocurrency.id, label='NEGATIVE').filter(func.date(Tweet.created_at) >= (datetime.today() - timedelta(days=d+1))).filter(func.date(Tweet.created_at) < (datetime.today() - timedelta(days=d))).count()
                    negative_articles = Article.query.filter_by(cryptocurrency_id=cryptocurrency.id, label='NEGATIVE').filter(func.date(Article.created_at) >= (datetime.today() - timedelta(days=d+1))).filter(func.date(Article.created_at) < (datetime.today() - timedelta(days=d))).count()
                    neg = negative_tweets+negative_articles
                elif(rType == 'tweets'):
                    pos = Tweet.query.filter_by(cryptocurrency_id=cryptocurrency.id, label='POSITIVE').filter(func.date(Tweet.created_at) >= (datetime.today() - timedelta(days=d+1))).filter(func.date(Tweet.created_at) < (datetime.today() - timedelta(days=d))).count()
                    neg = Tweet.query.filter_by(cryptocurrency_id=cryptocurrency.id, label='NEGATIVE').filter(func.date(Tweet.created_at) >= (datetime.today() - timedelta(days=d+1))).filter(func.date(Tweet.created_at) < (datetime.today() - timedelta(days=d))).count()
                else :
                    pos = Article.query.filter_by(cryptocurrency_id=cryptocurrency.id, label='POSITIVE').filter(func.date(Article.created_at) >= (datetime.today() - timedelta(days=d+1))).filter(func.date(Article.created_at) < (datetime.today() - timedelta(days=d))).count()
                    neg = Article.query.filter_by(cryptocurrency_id=cryptocurrency.id, label='NEGATIVE').filter(func.date(Article.created_at) >= (datetime.today() - timedelta(days=d+1))).filter(func.date(Article.created_at) < (datetime.today() - timedelta(days=d))).count()
                if(neg == 0):
                    neg = 1
                val = (pos/(pos+neg)*100)
                res.append(float("{:.2f}".format(val)))
            res = res[::-1]
            tab.append({
                'name': crypto.abbreviation,
                'data': res
            }) 
        return jsonify({
                'data': tab
            }), HTTP_200_OK
    return jsonify({
        'response': 'the cryptocurrency does not exist ! ! !'
    }), HTTP_404_NOT_FOUND