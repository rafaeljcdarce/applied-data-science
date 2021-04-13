import pandas as pd
import re
import us
from city_to_state import city_to_state_dict
import numpy as np
import geonamescache
from loc_ops import *


df = pd.read_csv('~/ADS/data/vaccinedata.csv', encoding = 'latin', header=None) # load example data
df.columns = ['id','author_id','author_handle','author_name','author_description','author_location','author_verified','text','is_reply','like_count','quote_count','reply_count','retweet_count','created_at','matched_rules']
df = df[20000:20200]
print(df['author_location'])
df = df.dropna(axis=0, subset=['author_location']).reset_index(drop=True)
locations = df['author_location']

raw_cleanLocs = [re.sub('[^a-zA-Z ,]+','',i) for i in locations] 

df['author_location'] = [clean_location(i) for i in raw_cleanLocs]
df = df.dropna(axis=0, subset=['author_location']).reset_index(drop=True)

df['Sentiment'] = np.random.uniform(-1, 1, len(df['author_location']))

locatedSentimentdf = pd.DataFrame({
            'Location': df['author_location'],
            'Sentiment': df['Sentiment'],
})
locatedSentimentdf.to_csv('locatedData.csv')
