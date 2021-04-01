import pandas as pd

def generate_time_series(df, freq='D', start=None, end=None, pos_label=1, neu_label=0, neg_label=-1):
    
    ts = []

    # if start is None:
    #     start = df.index.min()
    # if end is None:
    #     end = df.index.max()

    # rng = pd.date_range(start, end, freq=freq)
    for l in [pos_label, neu_label, neg_label]:
        t = df[df.sentiment == l]
        t = t.resample('D').agg({'sentiment':'size'}).fillna(0) 
        t = t.rename(columns={'sentiment':'count'})
        # t = t.reindex(rng, fill_value=0)
        ts.append(t)
    return ts

