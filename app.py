from flask import Flask, request
from flask_cors import CORS
import requests
import json
import pandas as pd
import pickle
import nltk
import re
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from langdetect import detect


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
    hastag = request.get_json()
    token_object = open("tokens.txt","r")
    access_token = token_object.readline()
    token_object.close()
    query = "https://api.twitter.com/2/tweets/search/recent?query=%23"+hastag['hashtag']+"&tweet.fields=created_at&max_results=100&expansions=author_id&user.fields=created_at"
    x = requests.get(query , headers={"Authorization":"Bearer "+access_token})

    tweets = pd.DataFrame(x.json()['data'])
    tweets['language'] = tweets['text'].apply(lambda x: detect(x))
    tweets = tweets.loc[tweets['language'] == "en"]
    f = open("model.pkl", 'rb')
    predict_model = pickle.load(f)
    tweets['text'] = tweets['text'].apply(tweet_cleaner)
    sentiments = predict_model.predict(tweets['text'])
    tweets['sentiment'] = sentiments
    print(tweets['sentiment'].value_counts())
    return '200'

if (__name__=='__main__'):
    app.run()
