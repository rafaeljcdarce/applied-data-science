from os import name
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

stopwords = nltk.corpus.stopwords.words("english") + ["coronavirus","covid","amp","vaccine","cases","new"]
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

def main():
    with open("data.pkl",'rb') as f:
        tweets = pickle.load(f)

    start = time.time()
    tweets["cleantext"] = tweets.text.apply(clean_tweet)
    print(f"Cleaned tweets in {time.time()-start}")

    # Combine all tweets for each date
    tweets["created_at"] = tweets["created_at"].dt.date
    docs = tweets.groupby("created_at")["cleantext"].apply(lambda x: " ".join(x)).reset_index()
    
    
    vectorizer = TfidfVectorizer(max_df=0.3)
    tfidf = vectorizer.fit_transform(docs["cleantext"])
    features = vectorizer.get_feature_names()

    df = pandas.DataFrame(tfidf.todense(),columns=features,index=docs["created_at"])
    df["tf-idf"] = df.apply(lambda x: top_labels(x), axis=1)
    df["tf-idf"].to_csv("tfidf.csv")


if __name__ == '__main__':
    main()
    