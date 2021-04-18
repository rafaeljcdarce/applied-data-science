import pandas as pd
from re import sub as re_sub
import us
from city_to_state import city_to_state_dict
import numpy as np
import geonamescache
from loc_ops import *
from pprint import pprint
from tqdm import tqdm
import multiprocessing as mp
import time

def sub(i, r='[^a-zA-Z ,]+', s=''):
    return re_sub(r,s,i)

def clean_locations(df, workers=7, chunksize=10000):
    # df = pd.read_pickle("~/applied-data-science/data.pkl") # read from pickle
    df.columns = ['id', 'location', 'text', 'date'] # set headers
    # df['date'] = pd.to_datetime(df['date']) # parse dates
    # df = df[20000:21000]

    df = df.dropna(axis=0, subset=['location']).reset_index(drop=True)
    # locations = df['location']

    print('\nPRE-PROCESSING\n')
    with mp.Pool(workers) as pool:
        df['clean_location'] = [i for i in pool.map(sub, tqdm(df['location']), chunksize = chunksize)]
        
    print('\nCLEANING\n')
    with mp.Pool(workers) as pool:
        df['clean_location'] = [i for i in pool.map(clean_location, tqdm(df['clean_location']), chunksize = chunksize)]

    # raw_cleanLocs = [sub('[^a-zA-Z ,]+','',i) for i in locations] 

    # df['cleaned location'] = [clean_location(i) for i in raw_cleanLocs]
    # df = df.dropna(axis=0, subset=['location']).reset_index(drop=True)
    # pprint(df[['location', 'cleaned location']])

    # df['Sentiment'] = np.random.uniform(-1, 1, len(df['location']))

    # locatedSentimentdf = pd.DataFrame({
    #             'Location': df['cleaned location'],
    #             'Sentiment': df['Sentiment'],
    # })
    # # locatedSentimentdf.to_pickle('locatedData.csv')
    # locatedSentimentdf.to_pickle('locateddf.pkl')
    # return locatedSentimentdf

    return df
