#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 17:47:27 2020

@author: lweiren
"""

from collections import namedtuple
from networkx import from_pandas_dataframe, set_node_attributes
import pandas as pd
import numpy as np

dataset = namedtuple("dataset", field_names = ["labelled_node_train", "stance_train", "unlabelled_node", "network"])

def load_node_data(df_adj_list, df_annotations, df_unlabelled):
    network = from_pandas_dataframe(df_adj_list, source="User_ID_x", target = "User_ID_y", edge_attr = ["Weights"] )
    
    for label in df_annotations.columns.values:
        set_node_attributes(network, values = pd.Series(df_annotations[label], index = df_annotations.index).to_dict(), name = label)
        
    labelled_node_train, stance_train = map(np.array, zip(*[([node],value["Stance"] == "Favour") for node, value in network.nodes(data=True) if value["Stance"] in ["Favour", "Against"]]))
    
    unlabelled_node = map(np.array, zip(*[([node]) for node, value in network.nodes(data=True) if value["Stance"] == "NONE"]))
    
    return dataset(labelled_node_train,stance_train,unlabelled_node,network)