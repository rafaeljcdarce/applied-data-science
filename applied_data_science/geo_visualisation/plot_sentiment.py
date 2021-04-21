import plotly.express as px
import pandas as pd 
import numpy as np
from pprint import pprint
# from .geocleaner import clean_locations
import os
from tqdm import tqdm
def plotGlobalSentiments(df=None, mode = 'states', threshold=None):
    
    df = splitDf(df=df, mode=mode)

    # if mode == 'countries':
    #     df = pd.read_pickle(os.getcwd()+'/applied_data_science/geo_visualisation/countriesdf.pkl')
    # elif mode == 'states':
    #     df = pd.read_pickle(os.getcwd()+'/applied_data_science/geo_visualisation/statesdf.pkl')
    
    unique_locations = df.Location.unique()

    # for each state, work out the proportion of positive sents 
    all_sentiments = {}
    pos_sentiments = {}
    for location, sentiment in zip(df['Location'], df['Sentiment']):
        try:
            all_sentiments[location] += 1
        except:
            all_sentiments[location] = 1
        if sentiment == 1:
            try:
                pos_sentiments[location] += 1
            except:
                pos_sentiments[location] = 1

    countries = []
    sentiments = []
    for country, sentiment in all_sentiments.items():
        prop = pos_sentiments[country]/sentiment
        if threshold:
            if prop > threshold:
                prop = 1
            else:
                prop = 0
        countries.append(country)
        sentiments.append(prop)


    # all_sentiments = {}
    # for location, sentiment in zip(df['Location'], df['Sentiment']):
    #     try:
    #         all_sentiments[location].append(sentiment)
    #     except:
    #         all_sentiments[location] = [sentiment]

    # countries = []
    # sentiments = []
    # for country, sentiment in all_sentiments.items():
    #     average_sentiment = np.average(sentiment)
    #     countries.append(country)
    #     sentiments.append(average_sentiment)

    countrySentimentsdf = pd.DataFrame({
        'Locations': countries,
        'Sentiment': sentiments
    })
    if mode == 'countries':
        fig = px.choropleth(countrySentimentsdf, locations="Locations",
                            color="Sentiment", 
                            color_continuous_scale='RdBu')
        fig.update_layout(
            title_text = 'Geographical Distribution of Sentiment across the World',
        )
    elif mode == 'states':
        fig = px.choropleth(countrySentimentsdf,
                    locations="Locations",
                    color="Sentiment",
                    locationmode = 'USA-states', color_continuous_scale='RdBu',
                    labels={'Sentiment':f'Proportion (thresh={threshold})'})

        fig.update_layout(
            title_text = 'Proportion of positive tweets for each US state',
            geo_scope='usa', 
        )
    # fig.show()
    # fig.write_image("images/"+mode+"Sentiments.pdf")
    return fig, all_sentiments


def splitDf(df=None, mode='states'):

    if not df:
        df = pd.read_pickle('locatedDf.pkl')

    # sentdf = pd.read_csv(os.getcwd()+'/applied_data_science/geo_visualisation/sentimentDf.pkl')
    # df['sentScore'] = sentdf['sentiment_score']
    # df['Sentiment'] = sentdf['sentiment']

    # statesdf = pd.DataFrame({'Location': [], 'Sentiment': []})
    # df.drop(columns=['id','location', 'text',])

    flag = mode == 'states'
    df = df[df['clean_location'].map(is_list)==flag]
    if flag:
        df['clean_location'] = df['clean_location'].map(get_state_code)

    # df = df[0:2000]
    # for i in tqdm(range(len(df))):
    #     if isinstance(df.clean_location.iloc[i], str):
    #         countriesdf = countriesdf.append({'Date': df.date.iloc[i], 'Location': df.clean_location.iloc[i], 'Sentiment': df.sent_scores.iloc[i]},ignore_index=True)
    #     elif isinstance(df.clean_location.iloc[i], list):
    #         statesdf = statesdf.append({'Date': df.date.iloc[i], 'Location': df.clean_location.iloc[i][3], 'Sentiment': df.sent_scores.iloc[i]},ignore_index=True)

    dff = pd.DataFrame({'Date': df['date'], 'Location': df['clean_location'], 'Sentiment': df['sents']})

    # statesdf.to_pickle('statesdf.pkl')
    # countriesdf.to_pickle('countriesdf.pkl')
    return dff

def is_list(obj):
    return isinstance(obj, list)

def get_state_code(location):
    return location[3]

# splitDf()
# plotGlobalSentiments('states')
