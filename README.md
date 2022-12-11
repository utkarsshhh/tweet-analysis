# tweet-analysis

This project is a web application that can predict and visualise the analytical information regarding any trend on [Twitter](https://twitter.com/home)


## Introduction

The objective of this application is to provide an analysis on any trending topics on twitter. The tweets in English language on any topic are fetched using the [Twitter API](https://developer.twitter.com/en/docs/twitter-api). The following analytical information is visualised in the application for the searched topic

1. The change in the number of tweets in a day or a week.
2. The current sentiment of the Tweeter's towards the topic. The sentiment is identified using a RandomClassifierModel trained on the data from [Kaggle](https://www.kaggle.com/datasets/saurabhshahane/twitter-sentiment-dataset).
3. The change in the average sentiment of the Tweeter's towards the topic over time.
4. The average tweets per a single user on the topic.


## Usage

### Installation

The Back-end code is built on Python 3.9 and the Front-end is built on Angular 14.2.7.. The IDE used in development of the back-end code is [PyCharm](https://www.jetbrains.com/pycharm/) and for the front-end it is [Visual Studio Code](https://code.visualstudio.com). The same IDE's can be used for the running the application by the users or any other IDE's supporting the mentioned environments.

