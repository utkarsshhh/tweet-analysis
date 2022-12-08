from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/get_tweets',methods = ['POST'])
def get_tweet():
    hastag = request.get_json()
    print (hastag)
    return '200'

if (__name__=='__main__'):
    app.run()
