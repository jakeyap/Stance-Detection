#!/usr/bin/env python
# coding: utf-8
from os.path import abspath, dirname
d = dirname(dirname(abspath(__file__)))


import sys
sys.path.insert(1, d+"/crawling/")
sys.path.insert(1, d+"/Recommenders/")
import time


import pandas as pd
from crawl_tweepy import findFollowers
import networkx as netx
import numpy as np

from fastai.collab import *
from fastai.tabular import *
from sklearn.model_selection import train_test_split

from reco_utils.evaluation.python_evaluation import rmse

    
def generateGraph(dest, file, file2, topic, file3, file4, file5):
    df_bn = pd.read_csv(file2)
    df = df_bn.copy()
    del df["User_ID"]
    df = df.drop_duplicates()

    df = df.sort_values(by=["Frequency (based on tweets)"], ascending=False).head(20)
    
    common_targets = set([tar for tar in df["Base Noun"]])
    
    
    # # How many people following First Neighbour
    
    df_1 = pd.read_csv(dest)
    df_2 = df_1.copy()
    
    
    df_r = pd.merge(df_1, df_2, how= "inner", on = ["1st_Neighbour"])
    df_rs = df_r.loc[df_r.User_ID_x != df_r.User_ID_y]
    df = df_rs.groupby(["User_ID_x", "User_ID_y"])["1st_Neighbour"].count().reset_index()
    df = df.rename(columns = {"1st_Neighbour": "Weights"})
    
    df.to_csv(file3)
    # Visualising Adjacency Matrix
    results = pd.crosstab(df_rs.User_ID_x, df_rs.User_ID_y)
    
    print("Shape: {}".format(results.shape))
    df_1 = pd.read_csv(file)

    
    
    df_1 = df_1[df_1["Targets"].isin(common_targets)]
    print("Before: {}".format(len(df_1.index.values.astype(int))))
    df_1 = df_1[df_1["User_ID"].isin(df_rs.User_ID_x)]
    df_1 = df_1[df_1["User_ID"].isin(df_rs.User_ID_y)]
    print("After: {}".format(len(df_1.index.values.astype(int))))

    df_1 = df_1.groupby(["User_ID", "Targets"])["Target's Polarity Score"].mean().reset_index()
    

    if(len(df_1[df_1.duplicated()]) != 0):
        print("Duplicate!!!!!!")
        print(df_1[df_1.duplicated()])
    
    df_features = df_1.pivot(index = "User_ID", columns = "Targets", values = "Target's Polarity Score")
    print(len(results),len(df_features))
    print(set(results.index.values.astype(int)).difference(set(df_features.index.values.astype(int))))
    print("leng a : {} , leng b: {}".format(len(set(df_features.index.values.astype(int))), len(set(results.index.values.astype(int)))))
    
    
    results.to_csv(file4)
    df_features.to_csv(file5)
    
    

def getFollowers(f1,f2,dest):

    df_bn = pd.read_csv(f1)
    df_tweet = pd.read_csv(f2)
    
    # Extract Top n Nouns set
    df = df_bn.copy()
    del df["User_ID"]
    df = df.drop_duplicates()
    print(df)
    df = df.sort_values(by=["Frequency (based on tweets)"], ascending=False).head(20) # SHould I do a Gini Index?????
    
    common_targets = set([tar for tar in df["Base Noun"]])
    
    df_user = df_tweet.copy()
    del df_user["Tweet_ID"]
    del df_user["Topic"]
    del df_user["Targets"]
    del df_user["Target's Polarity Score"]
    del df_user["Stance"] # only for annotated set
    df_user = df_user.drop_duplicates()
    
    
    #Construct Adjacency Matrix
    for noun in common_targets:
        df_temp = df_tweet[df_tweet["Targets"]== noun]
        users = df_temp["User_ID"]
        #ConstructGraph(users)
        cmp = int(len(users) * (len(users)-1) /2)
        print("{} : Length of users = {}, Number of Comparision: {} ".format(noun, len(users), cmp))
    
    # # Find the counts of user mention for each target
    df1 = pd.DataFrame({"C": df_bn.groupby(["User_ID","Base Noun"])["Base Noun"].count()}).reset_index()
    
    
    # # Find the count of user mentions for each common target
    df2 = df1[df1["Base Noun"].isin(common_targets)]
    #df2.sort_values(by=["User_ID"], ascending=True).head(20)
    
    
    df_qw = df_tweet[df_tweet["User_ID"].isin(set(df2.User_ID))].drop_duplicates("User_ID")
    print(df_qw)
    
    d = df_qw[df_qw["User_Follower_Counts"] < 5000]
    d = d[d["User_Follower_Counts"] > 100].count()
    
    total_num_mentions = max(df2.C)
    
    df2["C"] = df2["C"].apply(lambda x: x/total_num_mentions)
    df3 = pd.DataFrame({"C_max": df2.groupby(["User_ID"])["C"].max()}).reset_index()
    
    
    # # Find total number of different common targets the user mention
    df2 = pd.DataFrame({"C(m)": df2.groupby(["User_ID"])["User_ID"].count()}).reset_index()
    df2.sort_values(by=["C(m)"], ascending=False).head(20)
    df2["C(m)"] = df2["C(m)"].apply(lambda x: x/20)

    df_merge = df2.set_index("User_ID").join(df3.set_index("User_ID")).reset_index()
    alpha = 0.5
    beta = 1-alpha
    
    df_merge["Criteria_Score"] = alpha*df_merge["C(m)"] + beta * df_merge["C_max"]
    result_df= df_merge.sort_values(by="Criteria_Score", ascending = False).head(1000)

    columns = ["User_ID", "1st_Neighbour"]
    data = []
    
    
    for user in result_df.User_ID:
        follower_cnt = max(df_user[df_user["User_ID"] == user].User_Follower_Counts)
        if(follower_cnt <= 5000):
            l = findFollowers(user)
            if(len(l) ==0):
                time.sleep(120) # In case user cannot be found due to heavy traffic
                l = findFollowers(user)
            data.extend(l)
    
    df_final = pd.DataFrame(data, columns = columns)
    df_final.to_csv(dest, index = False)


def runningCL(dest,file1, file2,topic):
    
    df_bn = pd.read_csv(file2)
    df = df_bn.copy()
    del df["User_ID"]
    df = df.drop_duplicates()
   

    df = df.sort_values(by=["Frequency (based on tweets)"], ascending=False).head(20)
    
    common_targets = set([tar for tar in df["Base Noun"]])
    
    df_1 = pd.read_csv(file1)
    #print(df_1)
    df_f = pd.read_csv(dest)
    df_f2 = df_f.copy()
    
    df_r = pd.merge(df_f, df_f2, how= "inner", on = ["1st_Neighbour"])
    df_rs = df_r.loc[df_r.User_ID_x != df_r.User_ID_y]
    
    df_1 = df_1[df_1["Targets"].isin(common_targets)]
    print("Before: {}".format(len(df_1.index.values.astype(int))))
    df_1 = df_1[df_1["User_ID"].isin(df_rs.User_ID_x)]
    df_1 = df_1[df_1["User_ID"].isin(df_rs.User_ID_y)]
    print("After: {}".format(len(df_1.index.values.astype(int))))

    df_1 = df_1.groupby(["User_ID", "Targets"])["Target's Polarity Score"].mean().reset_index()
    
    train, test = train_test_split(df_1, test_size =0.2)
    
    train.to_csv(topic+ "_train_collab.csv", index = False)
    test.to_csv(topic+ "_test_collab.csv", index = False)
    
    data = CollabDataBunch.from_df(train, seed=42, valid_pct=0.2, bs= 8, num_workers=0)
    learn = collab_learner(data, n_factors=50, y_range=[-1,1], wd=1e-1)
    learn.fit_one_cycle(5, 1e-4)
    
    d= []
    
    for row in range(len(test)):
        
        pred = learn.predict(test.iloc[row])[0]
        d.append([test.iloc[row][0],test.iloc[row][1],test.iloc[row][2],pred.data])
        
    test = pd.DataFrame(d,columns=["User_ID", "Targets", "Target's Polarity Score", "CF_predict"])
    
    test_pred_y = test.copy()
    del test_pred_y["Target's Polarity Score"]
    print()

    test_actual_y = test.copy()
    del test_actual_y["CF_predict"]

    print("RSME: {}".format(rmse(test_actual_y,test_pred_y , col_user="User_ID", col_item="Targets", col_rating="Target's Polarity Score", col_prediction="CF_predict")))
    
    learn.save(topic+"_total_model", return_path=True)
    



