#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 09:45:45 2020

@author: theodorepender
"""
import tweepy
import numpy as np
import pandas as pd
import datetime
import pygsheets

"""
API key:
rqtmfuXV22syTLEVAEdBgsNCU

API secret key:
Ocsh8w2gfzouOkbyqjauAQ1kZe6R044xWWDmAk5Eb9q01V2GcT
"""
consumer_key        =  'rqtmfuXV22syTLEVAEdBgsNCU'
consumer_secret     = 'Ocsh8w2gfzouOkbyqjauAQ1kZe6R044xWWDmAk5Eb9q01V2GcT'
access_token        = '396576383-QERUE1UnYiXvg1u6ydc0NwAQYnQdkH42gTP5ecRi'
access_token_secret = 'bXMmGF6I2ZHv4GYaiakgYbb7GAyFDMV5nJslOoHrFL6e2'

if __name__ == '__main__':

    # ------------ Sign in ------------ #
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    # myStreamListener = MyStreamListener()
    # myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    # myStream.filter(track=['trump', 'covid', 'virus'], is_async=True)

    search_words = "biden"
    new_search = search_words + " -filter:retweets"
    
    #datetime.datetime.now()

    date_since = "2020-10-01"
    
    # Collect tweets
    tweets = tweepy.Cursor(api.search,
                  # q=new_search,
                  geocode="42.3601,71.0589,75km",
                  lang="en",
                  since=date_since).items(5)
    
    [tweet.text for tweet in tweets]
    
    # ----- analyze tweets ----- #
    
    # ----- read from google sheets ----- #
    gc = pygsheets.authorize(service_file='/Users/theodorepender/Desktop/Midnight-Labs-9d593d26ebe7.json')

    sh = gc.open('SentimentIndex')
    wks = sh[0]
    # ----- write to google sheets
    
    #open the google spreadsheet (where 'Recession-Indicator' is the name of my sheet)
    # for a new sheet, add data-editor@midnight-labs.iam.gserviceaccount.com as an editor and publish the sheet to web
    sh = gc.open('SentimentIndex')
    wks = sh[0]
    wks.set_dataframe(pd.DataFrame(),(1,1))





















