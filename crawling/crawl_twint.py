#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 10:31:06 2020

@author: lweiren
"""
import twint


def findUserid(uid):
    c = twint.Config()
    c.Username = uid
    c.Format = "ID {id} | Username {username}"
    
    twint.run.Lookup(c)
    
def findUsername(uid):
    c = twint.Config()
    c.User_id = uid
    c.Format = "ID {id} | Username {username}"
    
    twint.run.Lookup(c)

def findFollowers(name, limit =0):
    c = twint.Config()
    c.Username = name
    #c.User_full = True
    c.Store_object = True
    if(limit !=0):
        c.Limit = limit
    
    twint.run.Followers(c)
    followers = twint.output.follows_list
    return followers



def findFollowing(name):
    c = twint.Config()
    c.Username = name
    #c.User_full = True
    c.Store_object = True
    
    twint.run.Following(c)
    following = twint.output.follows_list
    return following

