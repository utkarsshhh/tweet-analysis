# tweet-analysis

This project is a web application that can predict and visualise the analytical information regarding any trend on [Twitter](https://twitter.com/home)


## Introduction

The objective of this application is to provide an analysis on any trending topics on twitter. The tweets in English language on any topic are fetched using the [Twitter API](https://developer.twitter.com/en/docs/twitter-api). The following analytical information is visualised in the application for the searched topic

1. The change in the number of tweets in a day or a week.
2. The current sentiment of the Tweeter's towards the topic. The sentiment is identified using a RandomClassifierModel trained on the data from [Kaggle](https://www.kaggle.com/datasets/saurabhshahane/twitter-sentiment-dataset). It is divided into three sentiments 1.0(Positive), 0.0(Neutral), -1.0(Negative)
3. The change in the average sentiment of the Tweeter's towards the topic over time.
4. The distribution of sentiments over the Tweeters.


## Usage

### Installation

The Back-end code is built on Python 3.9 and the Front-end is built on Angular 14.2.7.. The IDE used in development of the back-end code is [PyCharm](https://www.jetbrains.com/pycharm/) and for the front-end it is [Visual Studio Code](https://code.visualstudio.com). The same IDE's can be used for the running the application by the users or any other IDE's supporting the mentioned environments.
Angular can be installed by following the steps [here](https://angular.io/guide/setup-local) and Python can be downloaded from [here](https://www.python.org/downloads/).

### Data

The dataset for the sentiment classifier model is present in the file Twitter_Data.csv in the root folder.

### Code

The code is divided into three main sections:

#### 1. Front-end 
The front-end code is present in the __twitter-analysis__ folder in the root directory. The angular application can be run locally by running the following command in the terminal inside the twitter-analysis folder.

> ng serve

#### 2. Model
The model used for sentiment classification is a built using the jupyter notebook __Model_Selection.ipynb__ present in the root directory. Running the jupyter notebook will create the model __model.pkl__ and save it in the local machine.

#### 3. Back-end
The back-end is present in the __app.py__ file in the root directory. It can be run locally by running the following command in the terminal in the root folder

> python app.py

The Bearer Access token for the Twitter API is stored in a file tokens.txt 


### Libraries

The additional libraries used in Python are

#### 1. [pandas](https://pandas.pydata.org)
#### 2. [numpy](https://numpy.org/)
#### 3. [sqlite3](https://docs.python.org/3/library/sqlite3.html)
#### 4. [scikit-learn](https://scikit-learn.org/stable/)
#### 5. [pickle](https://docs.python.org/3/library/pickle.html)
#### 6. [nltk](https://www.nltk.org)
#### 7. [flask](https://flask.palletsprojects.com/en/2.2.x/)
#### 8. [Flask-Cors](https://flask-cors.readthedocs.io/en/latest/)
#### 9. [langdetect](https://pypi.org/project/langdetect/)

The additional libraries used in Angular are

#### 1. [chart.js](https://www.chartjs.org)


### How it Works

The landing page of the web application consists of a Search bar where the user can enter the topic(without the #) for which they want the analysis. On clicking "Search" button the application will fetch the tweets for past 7 days on the topic and display the analysis on the page.


## Conclusion

The analysis is displayed on the web application page. The detailed analysis can be found [here](https://medium.com/@utkarshpadia/how-to-perform-live-analysis-on-social-media-posts-for-any-topic-ecbb47f9560c)


