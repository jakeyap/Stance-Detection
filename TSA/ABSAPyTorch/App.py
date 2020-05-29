#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 10:59:34 2020

@author: lweiren
"""
from os import abspath, dirname
d = dirname(dirname(dirname(abspath(__file__))))



import torch
import sys
import spacy
#import neuralcoref


from POStagger import *
from TSA_infer import *
from cleaningTweets import *
from Objects import *


sys.path.insert(1, d+"/crawling/")
from crawl_twint import *

DELIMITER = "|"

# For filtering neutral polarity
L_POLARITY_THRES = -0.2
H_POLARITY_THRES = 0.2

nlp = spacy.load("en_core_web_sm")
neuralcoref.add_to_pipe(nlp)

def loadFile(topic, file):
    tweets= []
    
    
    f = open(file, "r")

    for line in f.readlines():
        fields = line.strip().split(DELIMITER)
        #print(fields)
        
        t = Tweet(fields[0],topic, fields[3])
        
        if(len(fields) > 5):
            t.stance = fields[5]
        else:
            t.stance = "NONE"
        
        u = User(fields[1],fields[2])
        u.username= fields[4]
        
        t.user = u
        tweets.append(t)
    f.close()
    
    return tweets

def sentimentCal(sen):
    polarity = 0
    for label, score in zip([-1,0,1],sen[0]):
        polarity += label * score
    #print(polarity)
    return polarity

def getTweets(topic, file):
     
    opt, tokenizer, model  = initialize()
    torch.autograd.set_grad_enabled(False)
    tweets = loadFile(topic, file)
    TOPIC = topic
    
    print("Topic : {}".format(TOPIC))
    
    #users = []
    base_nouns = set()
    
    for t in tweets:
        doc = nlp(t.org_content)
        
        #sentences = sentSegment(doc._.coref_clusters)
        sentences = sentSegment(t.org_content)
        t.clean_content = [cleaning(s) for s in sentences]
        
        
        for s in t.clean_content:
            sentObj = Sentence(s) 
            aspects = returnCandidateTargets(s, TOPIC)
            #print(aspects)
            
            for target in aspects:
                txt_left, aspect, txt_right = findingAspect(s, target)
                _, _ ,text_raw_bert_indices, aspect_bert_indices = prepare_data(txt_left,aspect, txt_right,tokenizer,opt)
                inputs = [text_raw_bert_indices, aspect_bert_indices]
                

                prob, _ = parseInput(model,inputs)
                polarity = sentimentCal(prob)
                
                a = Aspect(target, polarity)
                
                if(a.sen < L_POLARITY_THRES or a.sen > H_POLARITY_THRES):
                    sentObj.targets.append(a)
                    base_nouns.add(target.lower())
            
            if(len(sentObj.targets) != 0 ):
                t.sentences.append(sentObj)
        

        t.retrieveTargets()
        
    result_tweets = []
    for t in tweets:
        if(t.targets != None):
            result_tweets.append(t)

    print("Tweets processed: {}/{} , Polarised Tweets rate: {}%".format(len(result_tweets),len(tweets), len(result_tweets)/len(tweets)*100))
    return result_tweets, base_nouns #, users #, return users too!
