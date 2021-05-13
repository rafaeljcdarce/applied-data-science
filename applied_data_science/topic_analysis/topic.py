from os import name
import sys
import pickle
import pandas
import numpy as np

from sklearn.decomposition import LatentDirichletAllocation #Don't have this
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

import matplotlib.pyplot as plt
import seaborn as sns #Don't have this

import nltk #don't have this
import re
import string
import time

if len(sys.argv) < 2:
    print("Usage: topic.py dataset.pkl (clean)")
    exit()

dataset = sys.argv[1]
stopwords = nltk.corpus.stopwords.words("english")
stemmer = nltk.stem.SnowballStemmer("english")
removepunc = str.maketrans('','',string.punctuation+'’')
nTerms = 10

def clean_tweet(tweet):
    tweet = tweet.encode("ascii","ignore").decode().lower() #remove non ascii
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))',' ',tweet) #remove urls
    tweet = re.sub('@[^\s]+',' ',tweet) #remove @s
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet) #remove hashtags
    tweet = tweet.translate(removepunc) #remove punctuation
    tweet = re.sub('([0-9]+)', '', tweet) #remove numbers

    return ' '.join([word for word in tweet.split(' ') if word not in stopwords and len(word) > 3])

def top_labels(x):
    sort = (x[x>0].sort_values(ascending=False)[:nTerms])
    return list(zip(sort.index,sort))

def weird_dict(flat):
    out = {}
    for key in flat:
        if key[0] not in out.keys():
            out[key[0]] = key[1]
        else:
            out[key[0]] += key[1]

    return out 

def main():
    with open(dataset,'rb') as f:
        tweets = pickle.load(f)

    # Only run if the dataset is not clean (indicated by an extra arg 1 argument extra)
    if len(sys.argv) < 3:
        start = time.time()
        tweets["cleantext"] = tweets.text.apply(clean_tweet)
        print(f"Cleaned tweets in {time.time()-start}")
        with open("clean_"+dataset,'wb') as f:
            pickle.dump(tweets,f)



    # Combine all tweets for each date
    tweets["created_at"] = tweets["created_at"].dt.date
    tweets["created_at"] = pandas.to_datetime(tweets["created_at"])
    tweets = tweets[(tweets["created_at"] >= "2020-11-01") & (tweets["created_at"] <= "2021-03-28")]
    docs = tweets.groupby("created_at")["cleantext"].apply(lambda x: " ".join(x)).reset_index()
    
    print(tweets)
    # vectorizer = TfidfVectorizer(min_df=2,max_df=0.9)
    vectorizer = TfidfVectorizer(min_df=2)

    tfidf = vectorizer.fit_transform(docs["cleantext"])
    features = vectorizer.get_feature_names()
    # print(vectorizer.stop_words_)
    with open("stopwords.csv",'w') as f:
        f.write("\n".join(vectorizer.stop_words_))

    df = pandas.DataFrame(tfidf.todense(),columns=features,index=docs["created_at"])
    df["tf-idf"] = df.apply(lambda x: top_labels(x), axis=1)    
    df["tf-idf"].to_csv("tfidf.csv")
    flat = df["tf-idf"].explode().to_numpy().tolist()
    flat = weird_dict(flat)
    flat = sorted(flat.items(),key=lambda x: x[1],reverse=True)
    with open("tfidf-2.csv",'w') as f:
        f.writelines("\n".join([str(x) for x in flat]))


if __name__ == '__main__':
    main()
    