from flask.json import jsonify
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Flask, config, redirect, Response, stream_with_context
import os
from src.route.tweets import tweets
from src.route.tweets import upload as upload_tweets
from src.route.articles import articles
from src.route.reviews import reviews
from src.route.articles import upload as upload_articles
from src.route.cryptocurrencies import cryptocurrencies
from src.database import Article, db
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config
from flask_cors import CORS, cross_origin
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    CORS(app, origins="http://localhost:4200", allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials","Access-Control-Allow-Origin"],
    supports_credentials=True, intercept_exceptions=False)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            CORS_HEADERS='Content-Type',
            SWAGGER={
                'title': "Bookmarks API",
                'uiversion': 3
            }
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    JWTManager(app)
    app.register_blueprint(reviews)
    app.register_blueprint(tweets)
    app.register_blueprint(articles)
    app.register_blueprint(cryptocurrencies)
    Swagger(app, config=swagger_config, template=template)

    """
    def upload_articles_task():
        with app.app_context():
            upload_articles()
            print(time.strftime("Articles uploaded at : %A, %d. %B %Y %I:%M:%S %p"))
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=upload_articles_task, trigger="interval", seconds=4)
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    """
    """
    def upload_tweets_task():
        with app.app_context():
            upload_tweets()
            print(time.strftime("Tweets uploaded at : %A, %d. %B %Y %I:%M:%S %p"))
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=upload_tweets_task, trigger="interval", seconds=1)
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    """

    @app.get('/<short_url>')
    @swag_from('./docs/short_url.yaml')
    def redirect_to_url(short_url):
        article = Article.query.filter_by(short_url=short_url).first_or_404()
        if article:
            article.visits = article.visits+1
            db.session.commit()
            return redirect(article.url)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR

    return app
