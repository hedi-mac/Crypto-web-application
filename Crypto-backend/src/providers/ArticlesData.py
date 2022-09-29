from asyncio.windows_events import NULL
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from bs4 import BeautifulSoup
import os
import requests
import re 
from transformers import pipeline
import pandas as pd

class ArticlesData : 

    monitored_tickers = []
    summaries = []
    model_name = "human-centered-summarization/financial-summarization-pegasus"
    tokenizer = NULL
    model = NULL
    urls = NULL

    def __init__(self, monitored_tickers):
        self.API_KEY = os.environ.get("GOOGLE_API_KEY") 
        self.SEARCH_ENGINE_ID = os.environ.get("GOOGLE_SEARCH_ENGINE_ID") 
        self.monitored_tickers = monitored_tickers

    def configure(self):
        self.tokenizer = PegasusTokenizer.from_pretrained(self.model_name)
        self.model = PegasusForConditionalGeneration.from_pretrained(self.model_name)

    
    def get_urls(self, ticker, source, pages):
        hrefs = []
        start = (pages - 1) * 10 + 1
        url = f"https://www.googleapis.com/customsearch/v1?key={self.API_KEY}&cx={self.SEARCH_ENGINE_ID}&q={source}+{ticker}&tbm=nws&lr=lang_en&start={start}&dateRestrict=d32"
        data = requests.get(url).json()
        search_items = data.get("items")
        for i, search_item in enumerate(search_items, start=1):
            try:
                long_description = search_item["pagemap"]["metatags"][0]["og:description"]
            except KeyError:
                long_description = "N/A"
            #title = search_item.get("title")
            #snippet = search_item.get("snippet")
            hrefs.append(search_item.get("link"))
        return hrefs

    def search_for_stock_new_urls_google_api(self, ticker):
        hrefs = self.get_urls(ticker, "yahoo+finance", 3)
        #hrefs.extend(self.get_urls(ticker, "bloomberg", 1))
        return hrefs

    
    
    def search_for_stock_new_urls(self, tickers):
        search_url = "https://www.google.com/search?q=yahoo+finance+{}&tbm=nws&tbs=qdr:d&lr=lang_en".format(tickers)
        r = requests.get(search_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        atags = soup.find_all('a')
        hrefs = [link['href'] for link in atags]
        return hrefs
    
    def strip_unwanted_urls(self, urls, exclude_list):
        val = []
        for url in urls: 
            cond = 'https://' in url
            if cond and not any(exclude_word in url for exclude_word in exclude_list):
                res = re.findall(r'(https?://\S+)', url)[0].split('&')[0]
                val.append(res)
        return list(set(val))

    #Search and scrape cleaned URLS
    def scrape_and_process(self, URLs):
        ARTICLES = []
        for url in URLs: 
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            paragraphs = soup.find_all('p')
            date = soup.find('time')
            print(date)
            text = [paragraph.text for paragraph in paragraphs]
            words = ' '.join(text).split(' ')[:250]
            ARTICLE = ' '.join(words)
            ARTICLES.append(ARTICLE)
        return ARTICLES


    #Summarise all acrticles
    def summarize(self, articles):
        summaries = []
        for article in articles:
            input_ids = self.tokenizer.encode(article, return_tensors='pt')
            output = self.model.generate(input_ids, max_length=25, num_beams=5, early_stopping=True)
            summary = self.tokenizer.decode(output[0], skip_special_tokens=True)
            summaries.append(summary)
        return summaries
    
    def getData(self):
        self.configure()
        raw_urls = {ticker:self.search_for_stock_new_urls_google_api(ticker) for ticker in self.monitored_tickers}
        #Strip out unwanted URLS
        exclude_list = ['maps', 'policies', 'preferences', 'accounts', 'support']
        self.urls = {ticker:self.strip_unwanted_urls(raw_urls[ticker], exclude_list) for ticker in self.monitored_tickers}
        articles = {ticker:self.scrape_and_process(self.urls[ticker]) for ticker in self.monitored_tickers}
        self.summaries = {ticker:self.summarize(articles[ticker]) for ticker in self.monitored_tickers}
        for ticker in self.monitored_tickers:
            df = pd.DataFrame(self.summaries[ticker], columns=['Text'])
            self.summaries[ticker] = df.drop_duplicates()['Text'].to_numpy().tolist()
        return self.summaries

