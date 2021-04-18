import pandas as pd
from geocleaner import clean_locations
import time

df = pd.read_pickle("../../data.pkl")

print('Total tweet count: ', len(df))

t0 = time.time()
df = clean_locations(df, chunksize=1000)
t1 = time.time()

print('Time taken: ', t1-t0)
print('Number of tweets with non-empty location string : ', len(df))

print(df.head(20))

count = 0
for l in df['clean_location']:
    if l:
        count += 1
print('Number of tweets with cleaned locations', count)
