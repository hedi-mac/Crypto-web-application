from transformers import pipeline
import matplotlib.pyplot as plt
import pandas as pd
import re
import emoji 

class HuggingFaceTransformersAnalysis : 
    #Add sentiment analysis
    sentiment = pipeline('sentiment-analysis')

    def convertEmoji(self, txt):
        res = emoji.demojize(txt, delimiters=("", ""))
        res = re.sub('_', ' ', res)
        res = re.sub('-', ' ', res)
        return res

    def create_output_array(self, dataTweets, dataArticles, urls, monitored_tickers):
        scores = {ticker:self.sentiment(dataTweets[ticker]) for ticker in monitored_tickers}
        scoresArticles = {ticker:self.sentiment(dataArticles[ticker]) for ticker in monitored_tickers}
        label = []
        output = []
        colors = ["#FF8333", "#FF3371", "#33FF5E", "#AF7AC5", "#229954", "#1A5276"]
        i = 0
        for ticker in monitored_tickers:
            label = []
            for counter in range(len(dataTweets[ticker])):
                output_this = [
                    ticker,
                    dataTweets[ticker][counter],
                    "Twitter",
                    scores[ticker][counter]['label'],
                    scores[ticker][counter]['score']
                ]
                label.append(scores[ticker][counter]['label'])
                output.append(output_this)
            for counter in range(len(dataArticles[ticker])):
                try:
                    output_this = [
                        ticker,
                        dataArticles[ticker][counter],
                        urls[ticker][counter],
                        scoresArticles[ticker][counter]['label'],
                        scoresArticles[ticker][counter]['score']
                    ]
                    label.append(scoresArticles[ticker][counter]['label'])
                    output.append(output_this)
                except IndexError:
                    print('List index out of range')                 
            self.plotBars(label, colors[i], ticker)
            if i >= 5 :
                i = 0
            else : 
                i+=1
        scores = {ticker:self.sentiment(self.convertEmoji(dataArticles[ticker])) for ticker in monitored_tickers}            
        output.insert(0, ['Ticker', 'Text', 'URLs', 'label', 'score'])
        return output







