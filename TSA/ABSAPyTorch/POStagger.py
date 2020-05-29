#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 10:38:57 2020

@author: lweiren
"""
import sys
import spacy
from cleaningTweets import checkStopWordList

#sys.path.insert(1, "/home/lweiren/TweetNLP/ark-tweet-nlp-0.3.2/")


#from allennlp.predictors.predictor import Predictor
from nltk.tree import Tree
#from CMUTweetTagger import runtagger_parse

#MODEL_USED = "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo-constituency-parser-2018.03.14.tar.gz"

#predictor = Predictor.from_path(MODEL_USED)
nlp = spacy.load("en_core_web_sm")

# =============================================================================
# def returnCandidateTargets(text):
#     targets =[]
#     try:
#         jsonObj = predictor.predict(sentence=text)
#         t = Tree.fromstring(jsonObj["trees"])
#         for subtree in t.subtrees(filter = lambda x: x.label() == "NP"):
#             l = subtree.leaves()
#             if("." in subtree.leaves()):
#                 i = 0
#                 for token in subtree.leaves():
#                     if("." == token):
#                         print("HIIIITTT")
#                         l.remove(".")
#                         l[i-1] = l[i-1] + token
#                         print(subtree.leaves())
#                     i+=1
#             
#             string = " ".join(l)
#             if(string == "End lawless ClintonFoundation ."):
#                 print("Hit")
#             targets.append(string)
#             
#     except TypeError:
#         print(text)
#     return targets
# =============================================================================

# TWEET NLP VERSION (NOT TESTED)
# =============================================================================
# def returnCandidateTargets(text):
#     targets = []
#     result = runtagger_parse([text])[0]
#     for r in result:
#         #if(r[2] > 0.9):
#         if(r[1] == "N" or r[1] == "A" or r[1] == "^"):
#             if(checkStopWordList(r[0])):
#                 targets.append(r[0])
#     return targets
# =============================================================================
    
# SPACY VERSION     
def returnCandidateTargets(text, TOPIC):
    targets = []
    doc = nlp(text)
    for np in doc.noun_chunks:
        if(checkStopWordList(np.root.text, TOPIC) == True):
            targets.append(np.root.text)
# =============================================================================
#             if(np.root.text == "you" or np.root.text == "i" or np.root.text == "we"):
#                 print("Stopword: {}".format("np.root.text"))
# =============================================================================
    return targets

def findingAspect(text, target):
    start = text.find(target)
    if(start == -1):
        print("Invalid Target/Text: text = {} , target = {}".format(text, target))
        return None
    else:
        end = start + len(target)
        
    return [text[:start], text[start:end], text[end:]]

    
