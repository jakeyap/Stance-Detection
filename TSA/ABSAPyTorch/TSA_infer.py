#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# file: infer_example_bert_models.py
# author: songyouwei <youwei0314@gmail.com>
# fixed: yangheng <yangheng@m.scnu.edu.cn>
# Copyright (C) 2018. All Rights Reserved.
"""
Created on Fri Feb  7 09:21:26 2020

@author: lweiren
"""
import numpy as np
import torch
import torch.nn.functional as F
from models.lcf_bert import LCF_BERT
from models.aen import AEN_BERT
from models.bert_spc import BERT_SPC
from pytorch_transformers import BertModel
from data_utils import Tokenizer4Bert

model_classes = {
    'bert_spc': BERT_SPC,
    'aen_bert': AEN_BERT,
    'lcf_bert': LCF_BERT
}
# set your trained models here
state_dict_paths = {
    'lcf_bert': 'state_dict/lcf_bert_laptop_val_acc0.2492',
    'bert_spc': 'state_dict/bert_spc_laptop_val_acc0.268',
    'aen_bert': 'state_dict/aen_bert_twitter_val_acc0.7312'
}

class Parameter():

    def __init__(self, model_name,dataset):
        self.model_name = model_name
        self.dataset = dataset
        self.optimizer = "adam"
        self.initializer = "xavier_uniform_"
        self.learning_rate = 2e-5 # Possible Candidates: 2e-5/5e-5 (BERT), 1e-5 (non-BERT)
        self.dropout = 0.1
        self.l2reg = 0.01
        self.num_epoch = 10 # Possible Candidates: 10 (BERT), Larger Numbers (non-BERT)
        self.batch_size = 16 # Possible Candidates: 16, 32, 64 (BERT)
        self.log_step = 5
        self.embed_dim = 300
        self.hidden_dim = 300
        self.bert_dim = 768
        self.pretrained_bert_name = "bert-base-uncased"
        self.max_seq_len = int(80)
        self.polarities_dim = 3
        self.hops = 3
        self.device = None # can be set to cuda:0 if cuda exist, else cpu
        self.seed = None # set seed for reproducibility
        self.valset_ratio = float(0) # set ratio between 0 and 1 for validation support
        
        ## Only for LCF-BERT model
        self.local_context_focus = 'cdm' #local context focus mode: cdw or cdm
        self.SRD = 3 #semantic-relative-distance, see the paper of LCF-BERT model
    
def pad_and_truncate(sequence, maxlen, dtype='int64', padding='post', truncating='post', value=0):
    x = (np.ones(maxlen) * value).astype(dtype)
    if truncating == 'pre':
        trunc = sequence[-maxlen:]
    else:
        trunc = sequence[:maxlen]
    trunc = np.asarray(trunc, dtype=dtype)
    if padding == 'post':
        x[:len(trunc)] = trunc
    else:
        x[-len(trunc):] = trunc
    return x

def prepare_data(text_left, aspect, text_right, tokenizer, opt):
    text_left = text_left.lower().strip()
    text_right = text_right.lower().strip()
    aspect = aspect.lower().strip()
    
    text_raw_indices = tokenizer.text_to_sequence(text_left + " " + aspect + " " + text_right)            
    aspect_indices = tokenizer.text_to_sequence(aspect)
    aspect_len = np.sum(aspect_indices != 0)
    text_bert_indices = tokenizer.text_to_sequence('[CLS] ' + text_left + " " + aspect + " " + text_right + ' [SEP] ' + aspect + " [SEP]")
    text_raw_bert_indices = tokenizer.text_to_sequence(
        "[CLS] " + text_left + " " + aspect + " " + text_right + " [SEP]")
    bert_segments_ids = np.asarray([0] * (np.sum(text_raw_indices != 0) + 2) + [1] * (aspect_len + 1))
    bert_segments_ids = pad_and_truncate(bert_segments_ids, tokenizer.max_seq_len)
    aspect_bert_indices = tokenizer.text_to_sequence("[CLS] " + aspect + " [SEP]")
    
    text_raw_bert_indices = torch.tensor([text_raw_bert_indices], dtype=torch.int64).to(opt.device)
    aspect_bert_indices = torch.tensor([aspect_bert_indices], dtype=torch.int64).to(opt.device)

    return text_bert_indices, bert_segments_ids, text_raw_bert_indices, aspect_bert_indices

def get_parameters():
    return Parameter(model_name = "aen_bert", dataset = "twitter")

def initialize():
    

    opt = get_parameters()
    opt.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tokenizer = Tokenizer4Bert(opt.max_seq_len, opt.pretrained_bert_name)
    bert = BertModel.from_pretrained(opt.pretrained_bert_name)
    model = model_classes[opt.model_name](bert, opt).to(opt.device)
    
    print('loading model {0} ...'.format(opt.model_name))
    torch.autograd.set_grad_enabled(False)
    model.load_state_dict(torch.load(state_dict_paths[opt.model_name]))
    model.eval()
    torch.autograd.set_grad_enabled(False)
    
    return opt, tokenizer, model
    

def parseInput(model, inputs):
    outputs = model(inputs)
    t_probs = F.softmax(outputs, dim=-1).cpu().numpy()
    #print('t_probs = ', t_probs)
    #print(type(t_probs))
    sentiment = t_probs.argmax(axis=-1) - 1
    #print('aspect sentiment = ', t_probs.argmax(axis=-1) - 1)
    return (t_probs, sentiment)
    
    