from asyncio.windows_events import NULL
import os
import tweepy
from datetime import datetime
import re
import pandas as pd 

class TwitterData : 

    monitored_tickers = []
    twitter_auth_keys = NULL
    auth = NULL
    tweets = NULL

    def __init__(self, monitored_tickers):
        self.monitored_tickers = monitored_tickers

    def configure(self):
        self.twitter_auth_keys = {
            "consumer_key"        : os.environ.get("TWITTER_CONSUMER_KEY"),
            "consumer_secret"     : os.environ.get("TWITTER_CONSUMER_SECRET"),
            "access_token"        : os.environ.get("TWITTER_ACCESS_TOKEN"),
            "access_token_secret" : os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
            "bearer"              : os.environ.get("TWITTER_BEARER")
        }
        self.auth = tweepy.OAuthHandler(
                self.twitter_auth_keys['consumer_key'],
                self.twitter_auth_keys['consumer_secret']
        )
        self.auth.set_access_token (
                self.twitter_auth_keys['access_token'],
                self.twitter_auth_keys['access_token_secret']
        )

    #Clean the tweets : 
    def cleanTweet(self, twt):
        for ticker in self.monitored_tickers:
            twt = re.sub(f'#{ticker}', ticker, twt)
        twt = re.sub('#[A-Za-z0-9]+', '', twt)
        twt = re.sub('@[A-Za-z0-9]+', '', twt)
        twt = re.sub('\\n', '', twt)
        twt = re.sub('https:\/\/\S+', '', twt)
        return twt

    def getTweets(self, hashtag):
        api = tweepy.API(self.auth, wait_on_rate_limit=True)
        #search_term = f"#{hashtag} until:2022-11-01 -filter:retweets"
        search_term = f"#{hashtag} -filter:retweets"
        tweets = tweepy.Cursor(api.search_tweets, search_term, count=200, lang='en').items(100)
        return [self.cleanTweet(tweet.text) for tweet in tweets]

    def getData(self):
        self.configure()
        self.tweets = {ticker:self.getTweets(ticker) for ticker in self.monitored_tickers}
        for ticker in self.monitored_tickers:
            df = pd.DataFrame(self.tweets[ticker], columns=['Text'])
            self.tweets[ticker] = df['Text'].to_numpy().tolist()
        return self.tweets


