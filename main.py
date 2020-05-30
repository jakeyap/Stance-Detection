#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 14:31:28 2020

@author: lweiren
"""
import os

current_path = os.getcwd()
print(current_path)

import sys
sys.path.insert(1, current_path+"/TSA/")
sys.path.insert(1, current_path+"/TSA/ABSAPyTorch/")
sys.path.insert(1, current_path+"/crawling/")

import time

from getOldTweets import gatherUsersTweets, convertIDtoUsername, convertTweet
from Users_Social_Network import getFollowers, generateGraph, runningCL
from TSA_result import runTSASummary
from App import getTweets

import pandas as pd

keywords = {
    "Hillary_Clinton" : ["#gohillary", "#gohillary2016", "#hillary2016","#whyiamnotvotingforhillary", "#ohhillno", "#stophillary", "#hillary", "#hillaryclinton"],
    "Climate_Change_is_a_Real_Concern": ["#climatechange", "#globalwarming", "#climatechangescam", "#globalwarminghoax", "#junkscience",  "#globalcooling", "#globalwarmingisnotreal"],
    "Legalization_of_Abortion": ["#prochoice", "#abortion", "#prolife", "#praytoendabortion", "#EndAbortion", "#PlannedParenthood"],
    "Atheism": ["#prayer", "#faith", "#religion", "#atheism", "#atheist", "#Jesus", "#religionpoisoneverything", "#antireligion", "#NoMoreReligions", "#AntiTheism", "#antiatheist", "#normalizeatheism", "#ChristopherHitchens", "#secular", "#Humanism", "#secularism"],
    "Feminist_Movement" : ["#Feminists", "#FeministsAreUgly", "#INeedFeminismIsAwful"],
    "Donald_Trump": ["#DonaldTrump", "#wakeupamerica", "#trump2016"]
    }

def Menu():
    print("=========== TSA-Graph App ===========")
    print("1. Run entire process")
    print("2. Generate User-Labels")
    print("3. Crawl more Tweets based on Users")
    print("4. Run Collaborative filtering")
    print("5. Quit")
    print("=====================================")

def IOfiles():
    topic = input("Topic? ")
    data_fp = input("Dataset Filepath? ")
    directory = input("Save to which directory? ")
    
    return (topic, directory,data_fp)

def main():
    choice = -1
    while True:
        Menu()
        print("Enter choice:")
        choice = int(input())
        
        
        topic , directory , data_fp = IOfiles()
        topic = "_".join(topic.split())
        
        
        file1 = directory + "/" + topic +"_tweets.csv"
        file2 = directory+ "/" +topic +"_tweets_ave.csv"
        file3 = directory+ "/" +topic +"_polarity.csv"
        file4 = data_fp
        
        file5 = directory+"/" +topic +"_Followers.csv"
        file6 = directory +"/"+ topic +"_Users.csv"
        
        file7 = directory +"/"+ topic + "_user_tweets"
        file8 = directory +"/"+topic+ "_tweets_CF.csv"
        file9 = directory + "/" + topic +"_tweet_ave_CF.csv"
        file10 = directory + "/" + topic +"_polarity.csv"
        
        file11 = directory + "/" + topic +"_edgelist.csv"
        file12 = directory + "/" + topic +"_Adjacency_List.csv"
        file13 = directory + "/" + topic +"_features.csv"

            
        if choice == 1:
            #ALL 
          
            base_nouns = runTSASummary(topic,file1, file2, file3,file4)
            getFollowers(file3,file1 , file5)
            generateGraph(file5,file1, file3,topic, file11, file12, file13)
            
        
        elif choice == 2:
            
            df = pd.read_csv(file1)
            
            scores = {"FAVOR" : 1, "AGAINST": -1, "NONE": 0 }
            
            df["Stance Scores"] = [scores[v] for v in df["Stance"]]
            df1 = df.groupby(["User_ID"])["Stance Scores"].sum().reset_index()
            
            df1["User Stance"] = "FAVOUR"
            
            df1.loc[df1["Stance Scores"] < 0, "User Stance"] = "AGAINST"
            df1.loc[df1["Stance Scores"] == 0, "User Stance"] = "NONE"
            df1.to_csv(file6)
            
        elif choice == 3:
            
            df = pd.read_csv(file5)
            maxtweets = 500
            usernames = []
            l =[]
            for user_id in df.User_ID.unique():
                username = convertIDtoUsername(str(user_id))
                if username:
                    usernames.append(username)
                    try:
                        l.extend(gatherUsersTweets(username,keywords[topic], maxtweets))
                    except:
                        print("Debug: Sleeping for 10 mins for cooldown")
                        time.sleep(120)
                        l.extend(gatherUsersTweets(username,keywords[topic], maxtweets))
            
            with open(file7,'w') as file:
                for t in l:
                    file.write(convertTweet(t))
            
            
            tweets,base_nouns = getTweets(topic, file7)
            t_columns = ["Tweet_ID", "User_ID" , "User_Follower_Counts", "Topic","Targets", "Target's Polarity Score", "Stance"]
            t_data = []
            
            for tweet in tweets:
                t_data.extend(tweet.toDFTuple())
            
            df_tweet = pd.DataFrame(t_data, columns = t_columns)
            
            
            df_file1 = pd.read_csv(file1)
            df_file1 = pd.concat([df_file1,df_tweet], ignore_index=True)
            df_t = pd.DataFrame({"Mean_Polarity": df_file1.groupby(["Tweet_ID", "User_ID", "Targets"])["Target's Polarity Score"].mean()}).reset_index()
            
            df_file1.to_csv(file8) #file1 copy
            df_t.to_csv(file9) #file2 copy
            
            df_t["Polarity"] = "Positive"
            df_t.loc[df_t["Mean_Polarity"]< 0, "Polarity"] = "Negative"
            rank_df_col = ["Base Noun", "Frequency (based on tweets)", "Polarity Positive(%)", "Polarity Negative (%)", "User_ID"]
            
            data = []
            
            for noun in base_nouns:
                df = df_t[df_t["Targets"] == noun]
                users = df.User_ID
                pos_neg_groups = df.groupby(["Targets", "Polarity"]).Polarity.count()
                
                levels = [pos_neg_groups.index.levels[0].values, ["Positive", "Negative"]]
                new_index = pd.MultiIndex.from_product(levels, names=pos_neg_groups.index.names)
                pos_neg_groups = pos_neg_groups.reindex(new_index, fill_value = 0)
                
                pos_neg_counts = pos_neg_groups.tolist()
                freq = pos_neg_counts[0]+pos_neg_counts[1]
                pos_neg_counts.append(freq)
                for u in users:
                    data.append([noun, freq, pos_neg_counts[0]/freq*100, pos_neg_counts[1]/freq*100, u])
            
            df_pos_neg = pd.DataFrame(data, columns=rank_df_col)
            df_pos_neg.to_csv(file10, index = False)
            
        
        elif choice == 4:
            runningCL(file5,file8,file10,topic)
        elif choice == 5:
            break
        else:
            print("Invalid Input entered : {}".format(choice))

main()
