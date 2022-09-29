from src.HuggingFaceTransformersAnalysis import HuggingFaceTransformersAnalysis
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask import Blueprint, request
from flask_cors import cross_origin
from flask.json import jsonify
from src.providers.ArticlesData import ArticlesData
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.database import Article, Cryptocurrency, db
from flasgger import swag_from
from sqlalchemy import desc, asc
from datetime import datetime, timedelta
from sqlalchemy import func

articles = Blueprint("articles", __name__, url_prefix="/api/v1/articles")

@articles.get('/upload')
def upload():
    cryptocurrencies = Cryptocurrency.query
    monitored_tickers = []
    for cryptocurrency in cryptocurrencies:
        monitored_tickers.append(cryptocurrency.abbreviation)
    #Articles data : 
    data = ArticlesData(monitored_tickers)
    articlesData = data.getData()
    sentimentAnalysis = HuggingFaceTransformersAnalysis()
    scores = {ticker:sentimentAnalysis.sentiment(articlesData[ticker]) for ticker in monitored_tickers} 
    for ticker in monitored_tickers:
        label = []
        cryptocurrency = Cryptocurrency.query.filter_by(abbreviation=ticker).first()
        for counter in range(len(articlesData[ticker])):
            try:
                text = articlesData[ticker][counter]
                label = scores[ticker][counter]['label']
                score = scores[ticker][counter]['score']
                url = data.urls[ticker][counter]
                if not Article.query.filter_by(text=text).first():
                    article = Article(text=text, label=label, score=float(score), created_at=datetime(2022, 9, 3), url=url, cryptocurrency_id=cryptocurrency.id)
                    db.session.add(article)
                    db.session.commit()
            except IndexError:
                    print('List index out of range')   
    
    return jsonify({
        'response': 'articles uploded .'
    }), HTTP_201_CREATED


@articles.get('/')
@cross_origin(origin='localhost:4200',headers=['Content-Type','Authorization'])
def get_articles_by_cryptocurrency():
    crypto = request.args.get('crypto', '', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 0, type=int)
    cryptocurrency = Cryptocurrency.query.filter_by(abbreviation=crypto).first()
    if(cryptocurrency):
        days = request.args.get('days', 31, type=int)
        if(per_page == 0 ) : 
            articles = Article.query.order_by(desc(Article.created_at)).filter_by(cryptocurrency_id=cryptocurrency.id).filter(func.date(Article.created_at) >= (datetime.today() - timedelta(days=days))).filter(func.date(Article.created_at) <= (datetime.today()))
        else : 
            articles = Article.query.order_by(desc(Article.created_at)).filter_by(cryptocurrency_id=cryptocurrency.id).filter(func.date(Article.created_at) >= (datetime.today() - timedelta(days=days))).filter(func.date(Article.created_at) <= (datetime.today())).paginate(page=page, per_page=per_page)
            meta = {
                "page": articles.page,
                'pages': articles.pages,
                'total_count': articles.total,
                'prev_page': articles.prev_num,
                'next_page': articles.next_num,
                'has_next': articles.has_next,
                'has_prev': articles.has_prev
            }
        data = []
        for article in articles:
            data.append({
                'id': article.id,
                'text': article.text,
                'label': article.label,
                'score': article.score,
                'created_at': article.created_at,
                'url': article.url,
                'short_url': article.short_url,
                'visits': article.visits,
                'cryptocurrency': f'{article.cryptocurrency.name} - {article.cryptocurrency.abbreviation}'
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
        res = jsonify({'data': data, "meta": meta}), HTTP_200_OK
        return res
    return jsonify({
        'response': 'the cryptocurrency does not exist ! ! !'
    }), HTTP_404_NOT_FOUND



