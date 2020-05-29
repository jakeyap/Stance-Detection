#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 14:00:39 2020

@author: lweiren
"""

from twitter import *
import os
import tweepy
import datetime
import sys
import time

CONSUMER_KEY="A2FjDYLSKc8tfvGLcexZywK35"
CONSUMER_SECRET='kDR9HRGR54otDoAqp7XWFFbRIadUmG9g9li7aaY12qOnKQt2oK'

MY_TWITTER_CREDS = "/home/lweiren/TSA/ABSAPyTorch/.my_app_credentials"
if not os.path.exists(MY_TWITTER_CREDS):
    oauth_dance("Semeval sentiment analysis", CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)
oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
tobj = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))
# =============================================================================
# auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# api = tweepy.API(auth)
# # test authentication
# for tweet in tweepy.Cursor(api.search, q = "tweepy").items(10):
#     print(tweet.text)
# =============================================================================
l = []
i = 90000
pages = i / 100
max_id = -1
since_id = 0


for n in range(1):
    try:
        if(n == 0):
            searchresult = tobj.search.tweets(q = "Donald Trump lang:en -filter:retweets", count = 100, until = "2019-03-10")
            #since_id = searchresult["search_metadata"]["since_id"]
           
        else:
            searchresult = tobj.search.tweets(q = "Donald Trump lang:en -filter:retweets", count = 100 , max_id = max_id, until= "2019-03-10")
        lis = [tweet["id"] for tweet in searchresult["statuses"]]
        max_id =  lis[-1]
        #max_id = searchresult["search_metadata"]["max_id"]
    
        #print(searchresult["search_metadata"])
        #print(max_id)
        l.extend(lis)
    except:
        rate = tobj.application.rate_limit_status()
        reset = rate['resources']['statuses']['/statuses/show/:id']['reset']
        
        now = datetime.datetime.today()
        future = datetime.datetime.fromtimestamp(reset)
        seconds = (future-now).seconds+1
        
        if seconds < 10000:
            sys.stderr.write("Rate limit exceeded, sleeping for %s seconds until %s\n" % (seconds, future))
            time.sleep(seconds)


length= len(set(l))
