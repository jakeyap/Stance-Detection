#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 14:09:13 2020

@author: lweiren
"""
import os

current_path = os.getcwd()
# Preprocessing for tweets
import re
import preprocessor as p
import spacy
import nltk
from nltk.corpus import stopwords
import sys

sys.path.insert(1, current_path)
from AbbrTranslator import translator

stopwords = set(stopwords.words("english"))
stopwords.update(["people", "words", "word", "men", "woman", "amp","way", "look", "jr", "us", "americans", "years"])
nlp = spacy.load("en_core_web_sm")



def cleaning(string):
    #Emoji patterns
    emoji_pattern = re.compile("["
             u"\U0001F600-\U0001F64F"  # emoticons
             u"\U0001F300-\U0001F5FF"  # symbols & pictographs
             u"\U0001F680-\U0001F6FF"  # transport & map symbols
             u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
             u"\U00002702-\U000027B0"
             u"\U000024C2-\U0001F251"
             "]+", flags=re.UNICODE)
    string = emoji_pattern.sub(r"",string)
    string = re.sub("RT", "", string)
    string = re.sub("#", "", string)
    string = re.sub("\+", "", string)
    string = re.sub("\/", " or ", string)
    string = re.sub("&", " and ", string)
    string = re.sub("-", " ", string)
    string = re.sub("'", "", string)
    string = re.sub("ðŸ¤”","", string)
    string = re.sub("[¦]", "", string)
    string = re.sub("[()@:<>{}`=~|.,%_]",  " ", string)
    
    
    
    #Replace short-forms & Acronyms with proper English
 
    string = translator(string)

    p.set_options(p.OPT.EMOJI, p.OPT.SMILEY, p.OPT.MENTION)
    result = p.clean(string)
    return result

def checkStopWordList(word,TOPIC):
    common_words = [s.lower() for s in TOPIC.split()]
    stopwords.update(common_words)
    if word.lower() in stopwords:
        return False
    else:
        return True

def sentSegment(text):
    p.set_options(p.OPT.URL)
    #print(text)
    text = p.clean(text)
    doc = nlp(text)
    sents = []
    for sent in doc.sents:
        sents.append(sent.text)
    return sents