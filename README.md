# Stance-Detection

## Requirements
python == 3.7.6
fastai == 1.0.57
torch == 1.4.0
spacy == 2.1.8
nltk == 3.4.5
GetOldTweets3 == 0.0.11
twint == 2.8.0
python-twitter == 1.18.0
tweet-preprocessor == 0.5.0


## Crawling Username and UserIDs from the Annotated Tweets
1. Extract annonated tweets from annotated_compiled.txt
```sh
grep "|<topic>|" annotated_compiled.txt > <topic>.txt
```
E.g. grep "|Donald Trump|" annotated_compiled.txt

2. Change the input filepath in crawler.py

line 179: annotatedCrawl("/home/<usr>/Stance-Detection/Annotated_data/<topic>.txt")

3. Type the command as shown below
```sh
python crawler.py --out-tweet= <output-filepath>
```

E.g. python crawler.py --out_tweet= /home/<user>/Stance-Detection/Annotated_data/Donald_Trump_annot-out.txt

## Running TSA & get Social Network
1. Run "python main.py"
2. Enter Choice: 1
3. Fill in the prompts
E.g. 
Topic? Donald Trump
Dataset Filepath? "/home/lweiren/Stance-Detection/Annotated_data/Donald_Trump_annot-out.txt"
Save(d) to which directory? "/home/lweiren/Stance-Detection/test

Note: Please ensure that the pretrained aen_bert_twitter_val_acc0.7312 model exists in /home/<user>/Stance-Detection/TSA/ABSAPyTorch/state_dict/ before running Choice 1.
Note: The pretrained BERT model file exceeded 100MB file size limit in which GitHub allows. Thus, it will not be uploaded into GitHub. Link of model:  

## Crawling more tweets based on sampled users and Run TSA on them
1. Run "python main.py"
2. Enter Choice: 3
3. Fill in the prompts

E.g.
Topic? Donald Trump
Dataset Filepath? /home/<usr>/Stance-Detection/Annotated_data/Donald_Trump_annot-out.txt
Save(d) to which directory? /home/<usr>/Stance-Detection/test 

Note: Please ensure that Choice 1 was run previously and its output files exist in "/home/<usr>/Stance-Detection/<dir>"  before running Choice 3.
Note: Please ensure that the pretrained aen_bert_twitter_val_acc0.7312 model exists in /home/<user>/Stance-Detection/TSA/ABSAPyTorch/state_dict/ before running Choice 3.
Note: If User_IDs are constantly not found, it is probably caused by the browser: We've detected that JavaScript is disabled in your browser. Would you like to proceed to legacy Twitter?
This page intercepts the proper user's Twitter page which caused regex search to fail in finding the username. This is not a frequent bug during testing in April 2020-May 2020.

## Running Collaborative Filtering
1. Run "python main.py"
2. Enter Choice: 4
3. Fill in the prompts
E.g.
Topic? Donald Trump
Dataset Filepath? /home/<usr>/Stance-Detection/Annotated_data/Donald_Trump_annot-out.txt
Save(d) to which directory? /home/<usr>/Stance-Detection/test 

Note: Please ensure that Choice 1 & 3 was run previously and its output files exists in "/home/<usr>/Stance-Detection/<dir>"  before running Choice 4.
Note: If "Runtime Error" occurs due to Rank0Tensors, please repeat Step 1 - 3 without running Choice 1 or 3. The torch model in running TSA is probably affecting the CF torch model's train/evaluation mode.  