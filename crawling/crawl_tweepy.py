#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 10:52:44 2020

@author: lweiren
"""
import tweepy
import datetime 

CONSUMER_KEY="A2FjDYLSKc8tfvGLcexZywK35"
CONSUMER_SECRET='kDR9HRGR54otDoAqp7XWFFbRIadUmG9g9li7aaY12qOnKQt2oK'
ACCESS_TOKEN = "1216887691398144001-VbfxAB1j0GSofp7sdYeVQ44nBWuhQk"
ACCESS_TOKEN_SECRET = "lcwMgTfg3NXHGHyERneunzkkhDxkooCKsHowKHxrZF7DS"






#auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify= True)
usr_id_set = set()


def findFollowers(user_id):
    cursor = -1
    l = []
    try:
        for follower in tweepy.Cursor(api.followers_ids, user_id= user_id, count = 5000).items():
            l.append((user_id,follower))
# =============================================================================
#     except tweepy.RateLimitError:
#         #busyWaiting()
#         print(tweepy.RateLimitError)
# =============================================================================
    except:
        print("User not Found.")
        print("user_id: {}".format(user_id))
    return l

def showRelationship(user_id, target_id):
    try:
        result = api.show_friendship(source_id = user_id, target_id = target_id)
        print("--------------------")
        print("{} following {}: {}".format(user_id, target_id, result[0].following))
        print("{} follow by {}: {}".format(user_id, target_id, result[0].followed_by))
        return (result[0].following, result[0].following)
    except:
        print("User not Found.")
        print("user_id: {}".format(user_id))
        print("target_id: {}".format(target_id))



def findTweets(topic, num_tweets ,date_since = None, date_until = None):
    
    if(date_since != None):
        tweets = tweepy.Cursor(api.search, q=topic +" -filter:retweets", lang="en")
# =============================================================================
# def busyWaiting():
#     now = datetime.datetime.today()
#     future = datetime.datetime.fromtimestamp(reset)
#     seconds = (future-now).seconds+1
#     
#     if seconds < 10000:
#         sys.stderr.write("%s : Rate limit exceeded, sleeping for %s seconds until %s\n" % (flag, seconds, future))
#         time.sleep(seconds)
#     
# =============================================================================
#print(len(set(findFollowers(722528529716383744))))
#showRelationship(722528529716383744, 1033555419090825217)