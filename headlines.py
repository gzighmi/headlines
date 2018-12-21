import feedparser
from flask import Flask, render_template, request
import json
import urllib3
import urllib

#weatherAPIKey='8d5e9882741505248aed7274677054ae'

app = Flask(__name__)
BBCFeed = "http://feeds.bbci.co.uk/news/rss.xml"

RSSFeeds = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
                'cnn': 'http://rss.cnn.com/rss/edition.rss',
                'fox': 'http://feeds.foxnews.com/foxnews/latest'}

DEFAULTS = {'publication':'bbc', 'city':'London,UK'}

@app.route("/")

def home():
    #Get users headlines based on user input or defaults
    publication = request.args.get("publication")
    if not publication:
        publication = DEFAULTS['publication']
    articles = getNews(publication)

    #Get weather information based on user input or defaults
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = getWeather(city)

    return render_template("home.html", articles=articles, weather=weather)

def getNews(query):
    if not query or query.lower() not in RSSFeeds:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSSFeeds[publication])
    return feed['entries']


def getWeather(query):
    apiURL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=8d5e9882741505248aed7274677054ae"
    query = urllib.parse.quote(query)
    url = apiURL.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":
              parsed["weather"][0]["description"],
             "temperature":parsed["main"]["temp"],
             "city":parsed["name"],
             "country":parsed['sys']["country"]
              }
    return weather






if __name__ == '__main__':
    app.run(port=5000, debug=True)
