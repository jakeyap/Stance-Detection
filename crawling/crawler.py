#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 10:24:24 2020

@author: lweiren
"""
import sys
import os
from twitter import *
import time
import datetime
import argparse


parser = argparse.ArgumentParser(description="downloads tweets")
parser.add_argument('--out_tweet', dest='out_tweet', default=None, type=argparse.FileType('a'), required=True)

args = parser.parse_args()


# python crawler.py --out_tweet=TOPIC-out.txt 


CONSUMER_KEY="A2FjDYLSKc8tfvGLcexZywK35"
CONSUMER_SECRET='kDR9HRGR54otDoAqp7XWFFbRIadUmG9g9li7aaY12qOnKQt2oK'
COUNTS = 100                  # tweet per page - How increase trottle limit
USR_COUNT = 10000           # Number of followers return per page
PAGE_CNT = 1                # Number of pages returning Tweets
DELIMITER = "|"
tweet_id_set = set()
usr_id_set = set()
topics = []

MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')
if not os.path.exists(MY_TWITTER_CREDS):
    oauth_dance("Semeval sentiment analysis", CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)
oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
tobj = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))



class Tweet():
    
    def __init__(self, tid, uid, txt, ufc, un):
        self.tweet_id = tid
        self.user_id = uid
        self.user_name = un
        self.text = txt
        self.usr_followers_cnt= ufc
    
    def tolist(self):
        return [str(self.tweet_id), str(self.user_id),str(self.usr_followers_cnt), str(self.text), str(self.user_name)]


            
def query_topics():
    
    while(True):
        print("Enter topic: ")
        t = input()
        
        if(t.upper() == "Q"):
            break
        else:
            topics.append(t)


def determinePageCount():
   
    print("Enter Number of Tweets to retrieve:")
    num = input()
    if(num == 1):
      return 1
    return  int(num)//COUNTS + 1


def retrieveTweetbyID(string):
    l = string.split("|")
    try:
        tweet_SR = tobj.statuses.show(id = l[1], tweet_mode="extended")
        usr_id = tweet_SR["user"]["id"]
        username = tweet_SR["user"]["screen_name"]
        follow_cnts = tweet_SR["user"]["followers_count"]
        
        writeToFile([l[1],str(usr_id), str(follow_cnts), l[3], username ,l[4], l[5], l[6]],"i")
        
    except TwitterError as e:
            busyWaiting(e.e.code, "tID")



def retrieveTweets(topic):
    page = 1
    max_id = -1

    while True:
        try:
            if(page == 1):
                tweet_SR = tobj.search.tweets(q = topic+ " lang:en -filter:retweets", count = COUNTS, tweet_mode="extended")
            elif (page <= PAGE_CNT):
                tweet_SR = tobj.search.tweets(q = topic+ " lang:en -filter:retweets", count = COUNTS, max_id = max_id, tweet_mode="extended")
            else:
                break
            tnum = 1
            for tweet in tweet_SR["statuses"]:
                print("Tweet {}/{}".format(tnum, len(tweet_SR["statuses"])))
                if(tweet["id"] not in tweet_id_set):
                    tweet_id_set.add(tweet["id"])
                    text = tweet["full_text"].replace("\n", " ").replace("\r", " ")
                    text = text.encode("utf-8")
                    t = Tweet(tweet["id"], tweet["user"]["id"], text.decode("utf-8"), tweet["user"]["followers_count"], tweet["user"]["screen_name"])
                    writeToFile(t, "t")
                else:
                    print("Tweet Exists")
                tnum+=1
                print("===========================================================")
                    
            if(len(tweet_SR["statuses"]) > 0):
                max_id = tweet_SR["statuses"][-1]["id"]
            print("Page {}/{} completed in {} seconds".format(page,PAGE_CNT,tweet_SR["search_metadata"]["completed_in"]))
            page += 1
            
        except TwitterError as e:
            busyWaiting(e.e.code, "t")



def writeToFile(obj, flag):
    if flag == "t":
        out = DELIMITER.join(obj.tolist())
        args.out_tweet.write(out+"\n")
        
    elif flag == "i":
        out = DELIMITER.join(obj)
        args.out_tweet.write(out)
    
    else:
        print("WriteError: Invalid flag {}".format(flag))


def busyWaiting(ErrorCode, flag):
    
    if ErrorCode == 429:
                rate = tobj.application.rate_limit_status()
                reset = rate['resources']['statuses']['/statuses/show/:id']['reset']
                
                now = datetime.datetime.today()
                future = datetime.datetime.fromtimestamp(reset)
                seconds = (future-now).seconds+1
                
                if seconds < 10000:
                    sys.stderr.write("%s : Rate limit exceeded, sleeping for %s seconds until %s\n" % (flag, seconds, future))
                    time.sleep(seconds)

def annotatedCrawl(file):
    f = open(file, "r")
    i = 0
    for line in f.readlines():
        retrieveTweetbyID(line)
        i+=1
        print("{} Tweet(s) Done...".format(i))
    print("ALL DONE!")
    f.close()


# ===============================================================Hillary_Clinton_annot.txt"==============
# query_topics()
# if(len(topics) > 1):
#     num = int(2000/len(topics))
#     for topic in topics:
#         PAGE_CNT = int(num)//COUNTS + 1
#         retrieveTweets(topic)
# else:
#     PAGE_CNT = determinePageCount() # LoCAL UNBOUND For PAGE_CNT haven't handled
#     retrieveTweets(topics[0]) # Incompleted Function
# =============================================================================

annotatedCrawl("/home/lweiren/datasets/data/Legalization_of_Abortion_annot.txt")
