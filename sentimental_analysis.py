# -*- coding: utf-8 -*-
"""Sentimental Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LFpCtORvrIC-Z7utvAWjL6cdPFo35fJl

# **Sentimental Analysis on Twitter Data**
"""

# Import the libraries
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as пр
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

print(dir(tweepy))

"""# **Accessing Twitter**"""

# Load the data
from google.colab import files
uploaded = files.upload()

# Get the data
log = pd.read_csv('login.csv')
log

consumerKey = log['key'][0]
consumerSecret = log['key'][1]
accessToken = log['key'][2]
accessTokenSecret= log['key'][3]

authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)


authenticate.set_access_token(accessToken, accessTokenSecret)


#api = tweepy.API(authenticate, wait_on_rate_limit = True)
api = tweepy.API(authenticate)

"""# **Extraction of Tweets as Data Set**"""

tweets = api.user_timeline(screen_name="@elonmusk",count=200,include_rts = False,tweet_mode = 'extended')

for info in tweets[:3]:
     print("ID: {}".format(info.id))
     print(str(info.created_at))
     print(str(info.full_text))
     print("\n")

i = 0
for tweet in tweets:
  print(str(i) + ') '+tweet.full_text+ '\n')
  i=i+1

df = pd.DataFrame( [tweet.full_text for tweet in tweets] , columns=['Tweets'])


df.head()

"""# **Exploratory Data Analysis**"""

def cleanTxt(text):
  text = re.sub(r'@[A-Za-z0-9]+', '', text)
  text = re.sub(r'#','', text)
  text = re.sub(r'RT[\s]+', '', text)
  text = re.sub(r'https?:\/\/\S+', '', text)
  return text

df['Tweets']= df['Tweets'].apply(cleanTxt)

df

def getSubjectivity(text):
  return TextBlob(text).sentiment. subjectivity


def getPolarity(text):
  return TextBlob(text).sentiment.polarity


df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)

df

allWords = ' '.join( [twts for twts in df['Tweets']] )
wordCloud = WordCloud(width = 500, height=300, random_state = 21, max_font_size = 119).generate(allWords)
plt.imshow(wordCloud, interpolation = "bilinear")
plt.axis('off')
plt.show()

"""# **Polarity**"""

def getAnalysis(score):
    if (score < 0):
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

df['Analysis'] = df['Polarity'].apply(getAnalysis)

df

# Print all of the positive tweets
j=1
sortedDF = df.sort_values(by=['Polarity'])
for i in range(0, sortedDF.shape[0]):
    if(sortedDF['Analysis'][i] == 'Positive'):
          print(str(j) + ') '+sortedDF[ 'Tweets' ][i])
          print()
          j=j+1

j=1
sortedDF = df.sort_values(by=['Polarity'], ascending='False')
for i in range(0, sortedDF.shape[0]):
  if( sortedDF['Analysis' ][i] == 'Negative'):
     print(str(j) + ') '+ sortedDF['Tweets'][i])
     print()
     j= j+1

plt. figure(figsize=(8,6))
for i in range(0, df.shape[0]):
  plt.scatter(df['Polarity' ][i], df['Subjectivity'][i], color='Blue' )

plt.title('sentiment Analysis')
plt.xlabel( 'Polarity')
plt.ylabel( 'Subjectivity')
plt.show()

ptweets = df[df.Analysis == 'Positive']
ptweets = ptweets['Tweets']

round( (ptweets.shape[0]/df.shape[0]) *100 , 1)

ntweets = df[df.Analysis == 'Negative']
ntweets = ntweets['Tweets']

round( (ntweets.shape[0]/df.shape[0] *100), 1)

df['Analysis'].value_counts()

plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df['Analysis'].value_counts().plot(kind='bar')
plt.show()





