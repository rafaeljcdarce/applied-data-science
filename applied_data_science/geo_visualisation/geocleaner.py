import pandas as pd
import re
import us
from city_to_state import city_to_state_dict
import numpy as np
import geonamescache
from loc_ops import *


df = pd.read_csv('vaccinedata.csv', encoding = 'latin', header=None) # load example data
df.columns = ['id','author_id','author_handle','author_name','author_description','author_location','author_verified','text','is_reply','like_count','quote_count','reply_count','retweet_count','created_at','matched_rules']
df = df.dropna().reset_index(drop=True)
locations = df['author_location']

raw_cleanLocs = [re.sub('[^a-zA-Z ,]+','',i) for i in locations] 

df['author_location'] = [clean_location(i) for i in raw_cleanLocs]

print(df['author_location'].tail())
df.to_csv('locatedData.csv')
