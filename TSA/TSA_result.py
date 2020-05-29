
import os

current_path = os.getcwd()

import sys
sys.path.insert(1, current_path+"ABSAPyTorch/")
import pandas as pd

from App import *


def runTSASummary(topic,file1,file2,file3,file4):
    tweets, base_nouns = getTweets(topic,file4)
    t_columns = ["Tweet_ID", "User_ID" , "User_Follower_Counts", "Topic","Targets", "Target's Polarity Score", "Stance"]
    t_data = []
    
    for tweet in tweets:
        t_data.extend(tweet.toDFTuple())
    
    df_tweet = pd.DataFrame(t_data, columns = t_columns)

    
    df_t = pd.DataFrame({"Mean_Polarity": df_tweet.groupby(["Tweet_ID", "User_ID", "Targets"])["Target's Polarity Score"].mean()}).reset_index()


    df_tweet.to_csv(file1, index = False)
    
    df_t.to_csv(file2)
    
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
    df_pos_neg.to_csv(file3, index = False)
    return base_nouns
# To see base nouns without user IDs :  awk -F, '{print $1,$2;}' {Topic}_polarity.csv | uniq | sort -k2,2gr > {Topic}_Ranklist.txt