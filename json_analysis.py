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



f = open("sample.json")
data= json.load(f)
f.close()
texts = []
print (data)
tweets = pd.DataFrame(data['data'])
tweets['language'] = tweets['text'].apply(lambda x: detect(x))
print (tweets.shape)
tweets = tweets.loc[tweets['language']=="en"]
print (tweets.shape)
f= open("model.pkl",'rb')
predict_model = pickle.load(f)
tweets['text']= tweets['text'].apply(tweet_cleaner)
print(tweets['text'])

sentiments = predict_model.predict(tweets['text'])
tweets['sentiment'] = sentiments
print (tweets['sentiment'].value_counts())
tweets.to_csv("tweets.csv")