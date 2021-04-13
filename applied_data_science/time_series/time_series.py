import pandas as pd
from statsmodels.tsa.seasonal import STL
import matplotlib.pyplot as plt
import ruptures as rpt
import numpy as np

def get_time_series(df, freq='D', seasonal=True, trend=True, resid=True, period=7, pos_label=1, neu_label=0, neg_label=-1, sent_col='sents', norm=False):
    
    if not (seasonal or trend or resid):
        raise ValueError("At least one of seasonal, trend or residual must be True")

    ts = []

    if not isinstance(df, pd.DatetimeIndex): # check if indexed by date
        df = df.set_index('date')

    for l in [pos_label, neu_label, neg_label]:
        t = df[df[sent_col]== l] # filter by label
        t = t.resample(freq).agg({sent_col:'size'}).fillna(0) # count occurences (fill in missing dates with 0)
        t = t.rename(columns={sent_col:'count'})
        ts.append(t)

    # make sure all time series cover the same date range
    start = max([min(t.index.values) for t in ts])
    end = min([max(t.index.values) for t in ts])
    ts = [t.loc[start:end] for t in ts]

    # normalise based on total count (if required)
    if norm:
        total =  ts[0]['count'] + ts[1]['count'] + ts[2]['count']
        ts = [t.divide(total, axis=0) for t in ts]
        
    for i in range(len(ts)):
        # decompose time series
        components = STL(ts[i], period=period, robust=True).fit()

        # remove detected components as required
        for component, flag in zip(['trend', 'seasonal', 'resid'], [trend, seasonal, resid]):
            if not flag:
                comp = getattr(components, component)
                ts[i] = ts[i].subtract(comp, axis=0)

    return ts

def get_change_points(pos, neu, neg, pen=10, jump=1, min_size=2, plot=False):
    
    signal = (pos['count'].to_numpy(), neu['count'].to_numpy(), neg['count'].to_numpy())

    signal = np.stack(tuple(signal), axis=0).T
    
    cp = rpt.KernelCPD(kernel="rbf", jump=jump, min_size=min_size).fit_predict(signal, pen=pen)

    if plot:
        rpt.display(signal, cp, cp)
        plt.show()
    
    return pos.index.values[cp[:-1]]



