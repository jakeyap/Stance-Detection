#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 16:38:12 2020

@author: lweiren
"""


class Tweet_annot():
    
    def __init__(self, tid, topic, content, stance, op_twd, sen):
        self.tweet_id =tid
        self.topic =topic
        self.org_content = content
        self.clean_content = None
        
        self.stance =stance
        self.opinion_towards = op_twd
        self.sentiment = sen
        
#        self.hashtags = None
        
        self.sentences = []
        self.user = None
#        self.resulting_sen = []
class Tweet():
        
    def __init__(self, tid, topic, content):
        
        self.tweet_id =tid
        self.topic =topic
        self.org_content = content
        self.clean_content = None
        
        self.stance = None
        
#        self.hashtags = None
        
        self.sentences = []
        self.targets = None
        self.user = None
    
# =============================================================================
#     def computeSentiment(self):
#         l = []
# # =============================================================================
# #         for sent in self.sentences:
# #             sent.computeSentiment()
# #             result += sent.total_sen
# # =============================================================================
#         if(len(self.sentences) != 0):
#             for sent in self.sentences:
#                 sent.computeSentiment()
#                 l.append(sent.total_sen)
#             self.sen = cmpAbsSenValue(l)
#         print("Tweet: Num of Sentences = {}".format(len(self.sentences)))
# # =============================================================================
# #         if(len(l) == 0):
# #             print("Length l is 0!")
# # =============================================================================
#             #print(sen)
# =============================================================================
    
    def toDFTuple(self):
        l = []
        for t, t_sen in self.targets:
            #l.append([self.tweet_id, self.topic, self.sen, t, t_sen])
            l.append([self.tweet_id, self.user.uid, self.user.follower_cnts, self.topic, t, t_sen, self.stance])
        
        return l
    
    def retrieveTargets(self):
        result = []
        for sent in self.sentences:
            result.extend([(a.aspect.lower(), a.sen) for a in sent.targets])
        self.targets = result
        self.user.targets.extend(result)

class Sentence():
    def __init__(self, content):
        self.content = content
        self.targets=[]

    
# =============================================================================
#     def computeSentiment(self):
#         l = []
# # =============================================================================
# #         for aspect in self.targets:
# #             result += aspect.sen
# #         
# #         if(len(self.targets) != 0):
# #             self.total_sen = result / len(self.targets)
# # =============================================================================
#         for aspect in self.targets:
#             l.append(aspect.sen)
#         self.total_sen = cmpAbsSenValue(l)
#         if(self.total_sen == 0):
#             print("Content: {}".format(self.content))
#             print("Targets: {}".format(self.targets))
#             print("Sentence: {}".format(self.total_sen))
#     
# =============================================================================
    def toDFTuple(self, tweet_id):
        return [tweet_id, self.content]
    

class Aspect():
    def __init__(self, aspect, sen):
        self.aspect = aspect
        self.sen = sen
            

class User():
    
    def __init__(self, uid, follower_cnt):
        self.uid  = uid
        self.username = None
        
        
        self.follower_cnts = follower_cnt
        self.followers= None
        
#        self.following = None
#        self.following_cnts = fllow_cnts
        self.total_tweet_count = 0
        
        self.targets = []
        
    def __repr__(self):
        return "User(%s, %s)" % (self.uid, self.username)
    
    def __eq__(self, other):
        if isinstance(other, User):
            return ((self.uid == other.uid) and (self.uid == other.uid))
        else:
            return False
    
    def __hash__(self):
        return hash(self.__repr__())

# =============================================================================
# 
#     def computeSentiment(self, sen):
#         # How to Normalize to prevent it from exceeding 1
#          self.user_sum_sentiment += sen
# 
#     def calOverallSen(self):
#         if(self.total_tweet_count != 0):
#             self.overallSen = self.user_sum_sentiment / self.total_tweet_count
#          
# =============================================================================
        