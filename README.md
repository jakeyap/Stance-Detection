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

line 179: annotatedCrawl("/home/user/Stance-Detection/Annotated_data/<topic>.txt")

3. Type the command as shown below
```sh
python crawler.py --out-tweet= <output-filepath>
```

E.g. python crawler.py --out_tweet= /home/user/Stance-Detection/Annotated_data/Donald_Trump_annot-out.txt

### Description
These instructions crawls the missing user information we need: User_ID, Username, Follower Counts.

annontated_complied.txt contains the Semeval2016 dataset. In annotated_complied.txt, only Tweet_IDs, Topic, Tweet content, Stance, Target, Sentiment is available. The tweets that are in this textfile were crawled using the Semeval keywords.
 
These intructions will first crawl the user information, and then organise the tweets into different topics. Please do this before running Choice 1.

## Running TSA & get Social Network
1. Run "python main.py"

2. Enter Choice: 1

3. Fill in the prompts
```sh
E.g. 
Topic? Donald Trump
Dataset Filepath? "/home/lweiren/Stance-Detection/Annotated_data/Donald_Trump_annot-out.txt"
Save(d) to which directory? "/home/lweiren/Stance-Detection/test
```

4. Get the Ranklist of base_nouns by running
```sh
awk -F, '{print $1,$2;}' Topic_polarity.csv | uniq | sort -k2,2gr > Topic_Ranklist.txt
```
Note: Please ensure that the pretrained aen_bert_twitter_val_acc0.7312 model exists in /home/user/Stance-Detection/TSA/ABSAPyTorch/state_dict/ before running Choice 1.

Note: The pretrained BERT model file exceeded 100MB file size limit in which GitHub allows. Thus, it will not be uploaded into GitHub. Link of model:  https://drive.google.com/open?id=19tc-blUFAhc5JcNlc6sq8YSfYoKBD5q0

### Description
This Choice will run targeted sentiment analysis on each tweet. After that, the ranking of targets is done (line 90 -92, /TSA/Users_Social_Network.py) by extracting out the top 20 most frequency base nouns mentioned in terms of number of tweets. Using this ranking of targets, it will sample informative users and fetch their follower IDs. Lastly, it will construct the adjacency list of the sampled users.

```s
Output Files:

TSA results:
<Topic>_tweets.csv : Shows a list of tweets with their respective base nouns(targets) and their polarity scores.
<Topic>_tweets_ave.csv : Shows a list of tweets with their respective base nouns(targets) and their average polarity scores by grouping according to each Tweet_ID, User_ID pairs.
<Topic>_tweets_polarity.csv: Shows a list of base nouns(targets) , User_ID pairs and their ratio of no. of postive tweets to no .of negative tweets.
<Topic>_Ranklist.txt: Shows the frequency mentions of base_nouns from highest to lowest.

Social Network:
<Topic>_Adjacency_List.csv: Shows a user matrix which shows the number of shared followers between 2 users.
<Topic>_Followers.csv: Shows a list of users and their follower IDs.
<Topic>_edgelist.csv: Shows a list of user ID pairs and their number of shared neighbours.
<Topic>_features.csv: Shows a matrix between users and the base nouns mentioned where the values are the polarity scores.
```
## Crawling more tweets based on sampled users and Run TSA on them
1. Run "python main.py"

2. Enter Choice: 3

3. Fill in the prompts
```sh
E.g.
Topic? Donald Trump
Dataset Filepath? /home/user/Stance-Detection/Annotated_data/Donald_Trump_annot-out.txt
Save(d) to which directory? /home/user/Stance-Detection/test 
```

Note: Please ensure that Choice 1 was run previously and its output files exist in /home/user/Stance-Detection/test before running Choice 3.

Note: Please ensure that the pretrained aen_bert_twitter_val_acc0.7312 model exists in /home/user/Stance-Detection/TSA/ABSAPyTorch/state_dict/ before running Choice 3.


### Description
This Choice crawls more tweets for the sampled users which also contains the semeval keywords. As GetOldTweets3 is used, the user_ID was not available. Thus, user_IDs will be retrieved. TSA is then run on these new tweets and the results are concatenated with Topic_tweets.csv and Topic_polarity.csv. 

```sh
Output Files:

Crawled_Data:

<Topic>_additional_tweets.txt: Addtional tweets crawled

TSA results:
<Topic>_tweets_CF.csv: Combination results of the <Topic>_tweets.csv and the newly crawled tweets.
<Topic>_tweets_ave_CF.csv: Derived from <Topic>_tweets_CF.csv. Shows a list of tweets with their respective base nouns(targets) and their average polarity scores by grouping according to each Tweet_ID, User_ID pairs.
<Topic>_polarity_CF.csv: Derived from <Topic>_tweet_ave_CF.csv. Shows a list of base nouns(targets) , User_ID pairs and their ratio of no. of postive tweets to no .of negative tweets.
```

## Running Collaborative Filtering
1. Run "python main.py"

2. Enter Choice: 4

3. Fill in the prompts
```sh
E.g.
Topic? Donald Trump
Dataset Filepath? /home/user/Stance-Detection/Annotated_data/Donald_Trump_annot-out.txt
Save(d) to which directory? /home/user/Stance-Detection/test 
```

Note: Please ensure that Choice 1 & 3 was run previously and its output files exists in /home/user/Stance-Detection/test before running Choice 4.

Note: If "Runtime Error" occurs due to Rank0Tensors, please repeat Step 1 - 3 without running Choice 1 or 3. The torch model in running TSA is probably affecting the CF torch model's train/evaluation mode.

### Description
This Choice runs Collaborative Filtering using fastai's collab learner model. First, the top 20 most frequent base nouns are resampled (derived from Topic_polarity_CF.csv). Users from Topic_tweets_CF.csv are also resampled according to the new top 20 base nouns. The polarity scores of the base nouns are then averaged based on the newly sampled users. This is then feeded into the CF model to work on a user level. The processed dataset is splitted into a test set (20%) and training set (80%). The CF model is then trained for 5 epochs and then evaluated using Root Mean Square Error (evaluation is done at user level). 


```sh
Output Files:
<Topic>_train_collab.csv: Training set for CF Model
<Topic>_test_collab.csv: Test set for CF Model
<Topic>_total_model.pth: CF model
RSME score is printed in terminal.
```
