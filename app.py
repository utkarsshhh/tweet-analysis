# Importing the libraries
from flask import Flask, request
from flask_cors import CORS
import requests
import pandas as pd
import numpy as np
import pickle
import nltk
import re
from datetime import datetime,timedelta,date,timezone
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from langdetect import detect

# Defining the Flask app

app = Flask(__name__)
CORS(app)


def tokenize(text):
    '''

    This function processes the text by removing stopwords, tokenizing the sentences and lemmatizing words to
    make the text usable for further transformation

    Input:
    text - a string(tweet) which is the input of the model

    Output:
    returns the input text as clean tokens in a list


    '''

    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    tokenized_text = [lemmatizer.lemmatize(token).strip() for token in tokens]
    return tokenized_text

def string_to_time(string):

    '''

    This function converts the input time string to a datetime object

    Input:
    string: a time string to be converted to datetime object

    Output:
    returns the datetime object of the string

    '''

    return datetime.strptime(string,"%Y-%m-%dT%H:%M:%S.%fZ")


def seperate_count(tweets):
    '''

        This function is used to fetch the date from datetime object and group the data
        according to the date

        Input:
        tweets: a dataframe containing the tweets and their timestamp and other metadata

        Output:
        returns a dictionary with the count of records for each date

        '''

    tweets['created_at'] = tweets['created_at'].apply(string_to_time)
    tweets['date'] = tweets['created_at'].apply(lambda x: str(x.date()))
    grouped_tweets = tweets.groupby(by='date').count()
    labels = np.array(grouped_tweets.index)
    counts = np.array(grouped_tweets['id'])
    return {'labels':labels.tolist(),'counts':counts.tolist()}

def get_sentiment(tweets):
    '''

        This function finds the average sentiment of the tweets and returns it in
        the form of a string

        Input:
        tweets: a dataframe containing the tweets and their sentiment

        Output:
        sentiment: a string which is the overall sentiment of the topic

    '''

    tweet_sentiments = tweets['sentiment'].value_counts()
    try:
        positive_counts = tweet_sentiments.loc[1.0]
    except:
        positive_counts = 0
    try:
        negative_counts = tweet_sentiments.loc[-1.0]
    except:
        negative_counts = 0
    try:
        neutral_counts = tweet_sentiments.loc[0.0]
    except:
        neutral_counts = 0


    if (positive_counts + negative_counts < neutral_counts):
        avg_sentiment = tweets.loc[tweets['sentiment'] != 0.0]['sentiment'].mean()
        if (avg_sentiment > 0.6):
            sentiment = "Positive"
        elif (avg_sentiment < 0.6 and avg_sentiment > 0.4):
            sentiment = "Neutral"
        else:
            sentiment = "Negative"
    else:
        avg_sentiment = tweets['sentiment'].mean()
        if (avg_sentiment > 0.5):
            sentiment = "Positive"
        elif (avg_sentiment < 0.5 and avg_sentiment > 0.3):
            sentiment = "Neutral"
        else:
            sentiment = "Negative"
    return(sentiment)

def sentiment_distribution(tweets):
    '''

        This function idetifies the lables and counts of each label(sentiment) for visualisation

        Input:
        tweets: a dataframe containing the tweets and their sentiment

        Output:
        returns a dictionary with the count of records for each sentiment

    '''

    grouped_tweets = tweets.groupby(by='sentiment').count()
    labels = np.array(grouped_tweets.index)
    counts = np.array(grouped_tweets['id'])
    return {'pieLabels': labels.tolist(), 'pieCounts': counts.tolist()}


def seperate_sentiments(tweets):
    '''

        This function is used to calculate the average sentiment for each date and group the data
        according to the date

        Input:
        tweets: a dataframe containing the tweets and their timestamp and other metadata

        Output:
        returns a dictionary with the average sentiment of tweets for each date

    '''

    tweets['date'] = tweets['created_at'].apply(lambda x: str(x.date()))
    grouped_tweets = tweets.loc[tweets['sentiment'] != 0.0][['date', 'sentiment']].groupby(by="date").mean()
    sentiment_labels = np.array(grouped_tweets.index)
    sentiments = np.array(grouped_tweets['sentiment'])
    return {'sentimentLabels':sentiment_labels.tolist(),'sentiments':sentiments.tolist()}

def detect_language(text):
    '''

        This function detects the language of the tweet using langdetect

        Input:
        text: the string for which the language is to be detected

        Output:
        lang: returns the language as a string for the text input

    '''

    try:
        lang = detect(text)
    except:
        lang = ""
    return lang


def tweet_cleaner(text):

    '''

    This function is used to clean the tweets fetched from the API. It removes the URL's, user mentions
    and # special character.

    Input:
    text - a string(tweet) for which the sentiment is to be predicted

    Output:
    cleaned_text - returns the input string in a cleaned format.

    '''


    text = re.sub('http://\S+|https://\S+', '', text)
    cleaned_text = text[text.find(":")+1:]
    cleaned_text = cleaned_text.replace("#","")
    split_arr = cleaned_text.split()
    cleaned_arr =[]
    for i in range(len(split_arr)):
        if (split_arr[i].find("@") == -1):
            cleaned_arr.append(split_arr[i])
    cleaned_text = " ".join(cleaned_arr)

    return cleaned_text

@app.route('/get_tweets',methods = ['POST'])
def get_tweet():
    # Fetching the token Bearer token for authentication of API
    hashtag = request.get_json()
    token_object = open("tokens.txt","r")
    access_token = token_object.readline()
    token_object.close()

    # Defining the process for fetching tweets for a whole week.
    further_pages = True
    today = datetime.now(timezone.utc)
    week_start = today - timedelta(days=6)
    time_now = today - timedelta(seconds=20)
    time_string = str(time_now.time()).split(".")[0]
    end_date = str(today.date()) + "T" + time_string + "Z"
    start_date = str(week_start.date()) + "T00:00:00Z"
    query1 = "https://api.twitter.com/2/tweets/search/recent?query=%23"+hashtag['hashtag']+"&tweet.fields=created_at&max_results=100&expansions=author_id&user.fields=created_at&start_time="+start_date+"&end_time="+end_date # The Twitter API query
    x = requests.get(query1, headers={"Authorization": "Bearer " + access_token})
    tweets = pd.DataFrame(x.json()['data'])
    # Making API request repeatedly to fetch all tweets from paginated results of the API call
    while (further_pages):
        try:
            next_token = x.json()['meta']['next_token']
            query2 = "https://api.twitter.com/2/tweets/search/recent?query=%23" + hashtag['hashtag'] + "&tweet.fields=created_at&max_results=100&expansions=author_id&user.fields=created_at&start_time="+start_date+"&end_time="+end_date+"&pagination_token="+next_token
            x = requests.get(query2, headers={"Authorization": "Bearer " + access_token})
            page_tweets = pd.DataFrame(x.json()['data'])
            df_array = [tweets,page_tweets]
            tweets = pd.concat(df_array)
        except:
            further_pages = False


    # Cleaning the text tweet to make it usable for the model
    tweets['text'] = tweets['text'].apply(tweet_cleaner)
    tweets['language'] = tweets['text'].apply(lambda x: detect_language(x))
    tweets = tweets.loc[tweets['language'] == "en"]
    f = open("model.pkl", 'rb')
    predict_model = pickle.load(f)

    #Predicting the sentiment of the tweets using the pickle model
    sentiments = predict_model.predict(tweets['text'])
    tweets['sentiment'] = sentiments
    #Organising data and predictions for visualisation in the web application
    tweet_analysis = seperate_count(tweets)
    tweet_analysis['sentiment'] = get_sentiment(tweets)
    pie_chart_distribution = sentiment_distribution(tweets)
    tweet_analysis['pieLabels'] = pie_chart_distribution['pieLabels']
    tweet_analysis['pieCounts'] = pie_chart_distribution['pieCounts']
    sentiment_variation = seperate_sentiments(tweets)
    tweet_analysis['sentimentLabels'] = sentiment_variation['sentimentLabels']
    tweet_analysis['sentiments'] = sentiment_variation['sentiments']
    return tweet_analysis
if (__name__=='__main__'):
    app.run()
