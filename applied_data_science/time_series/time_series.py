import pandas as pd

def generate_time_series(df, freq='D', start=None, end=None, pos_label=1, neu_label=0, neg_label=-1, sent_col='sents'):
    
    ts = []
    if not isinstance(df, pd.DatetimeIndex):
        df = df.set_index('date')
    # if start is None:
    #     start = df.index.min()
    # if end is None:
    #     end = df.index.max()

    # rng = pd.date_range(start, end, freq=freq)
    for l in [pos_label, neu_label, neg_label]:
        t = df[df[sent_col]== l]
        t = t.resample('D').agg({sent_col:'size'}).fillna(0) 
        t = t.rename(columns={sent_col:'count'})
        # t = t.reindex(rng, fill_value=0)
        ts.append(t)
    return ts

