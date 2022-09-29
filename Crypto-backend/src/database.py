from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import AbstractConcreteBase, declared_attr, as_declarative
from datetime import datetime
import string
import random

db = SQLAlchemy()

class Cryptocurrency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    abbreviation = db.Column(db.String(10), nullable=False)
    articles = db.relationship('Article', back_populates="cryptocurrency")
    tweets = db.relationship('Tweet', back_populates="cryptocurrency")

class Review(AbstractConcreteBase, db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    label = db.Column(db.String(10), nullable=False)
    score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    __mapper_args__ = {
        'polymorphic_identity': 'review',
        "concrete": True
    }

class Tweet(Review):
    __tablename__ = "tweet"
    id = db.Column(db.Integer, db.ForeignKey("review.id"), primary_key=True, autoincrement=True)
    cryptocurrency_id = db.Column(db.ForeignKey('cryptocurrency.id'))
    cryptocurrency = db.relationship("Cryptocurrency", back_populates="tweets")
    __mapper_args__ = {
        'polymorphic_identity':'tweet',
        'with_polymorphic': '*',
        "concrete": True
    }

class Article(Review):
    __tablename__ = "article"
    id = db.Column(db.Integer, db.ForeignKey("review.id"), primary_key=True, autoincrement=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=True)
    visits = db.Column(db.Integer, default=0)
    cryptocurrency_id = db.Column(db.ForeignKey('cryptocurrency.id'))
    cryptocurrency = db.relationship("Cryptocurrency", back_populates="articles")

    def generate_short_characters(self):
        characters = string.digits+string.ascii_letters
        picked_chars = ''.join(random.choices(characters, k=3))
        link = self.query.filter_by(short_url=picked_chars).first()
        if link:
            self.generate_short_characters()
        else:
            return picked_chars

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_characters()

    __mapper_args__ = {
        'polymorphic_identity':'article',
        'with_polymorphic': '*',
        "concrete": True
    }

