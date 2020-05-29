#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:52:17 2020

@author: lweiren
"""
import GetOldTweets3 as got
import re
import requests

def gatherUsersTweets(users, keywords, maxtweets):
    query = " OR ".join(keywords)

    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query) \
                                               .setMaxTweets(maxtweets)\
                                              .setUsername(users)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    
    return tweets

def convertIDtoUsername(user_id):
    r = requests.get('https://twitter.com/intent/user?user_id=' + user_id)
    #print(r.content.decode('utf-8'))
    user_search=re.search('<title>.*\(@(.*)\).*</title>', r.content.decode('utf-8'), re.IGNORECASE)
    #print(user_search.group(1))
    if(user_search):
        username = user_search.group(1)            
        return username
    else:
        print("ID %s not found" % user_id)
        return None
def convertTweet(tweet):
    return "|".join([str(tweet.id), str(tweet.author_id), "-1", tweet.text, tweet.username]) + "\n"

users = ["votenickmoutos", "yunfeiw504"]
keywords = ["#prolife", "#Jesus"]
maxtweets = 1
t = gatherUsersTweets(users, keywords, maxtweets)[0]
