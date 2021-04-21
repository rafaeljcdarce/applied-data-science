import plotly.express as px
import pandas as pd 
import numpy as np
from pprint import pprint
# from .geocleaner import clean_locations
import os
from tqdm import tqdm
def plotGlobalSentiments(mode, df=0):

    if mode == 'countries':
        df = pd.read_pickle(os.getcwd()+'/applied_data_science/geo_visualisation/countriesdf.pkl')
    elif mode == 'states':
        df = pd.read_pickle(os.getcwd()+'/applied_data_science/geo_visualisation/statesdf.pkl')
    unique_locations = df.Location.unique()

    all_sentiments = {}
    for location, sentiment in zip(df['Location'], df['Sentiment']):
        try:
            all_sentiments[location].append(sentiment)
        except:
            all_sentiments[location] = [sentiment]

    countries = []
    sentiments = []
    for country, sentiment in all_sentiments.items():
        average_sentiment = np.average(sentiment)
        countries.append(country)
        sentiments.append(average_sentiment)

    countrySentimentsdf = pd.DataFrame({
        'Locations': countries,
        'Sentiment': sentiments
    })
    if mode == 'countries':
        fig = px.choropleth(countrySentimentsdf, locations="Locations",
                            color="Sentiment", 
                            color_continuous_scale=px.colors.sequential.Plasma)
        fig.update_layout(
            title_text = 'Geographical Distribution of Sentiment across the World',
        )
    elif mode == 'states':
        fig = px.choropleth(countrySentimentsdf,
                    locations="Locations",
                    color="Sentiment",
                    locationmode = 'USA-states', color_continuous_scale=px.colors.sequential.Plasma)

        fig.update_layout(
            title_text = 'Geographical Distribution of Sentiment across the United States',
            geo_scope='usa', 
        )
    # fig.show()
    fig.write_image("images/"+mode+"Sentiments.pdf")
    return fig


def splitDf(df=0):
    if df == 0:
        df = pd.read_pickle(os.getcwd()+'/applied_data_science/geo_visualisation/locatedData.pkl')
    # sentdf = pd.read_csv(os.getcwd()+'/applied_data_science/geo_visualisation/sentimentDf.pkl')
    # df['sentScore'] = sentdf['sentiment_score']
    # df['Sentiment'] = sentdf['sentiment']
    countriesdf = pd.DataFrame({'Date': [], 'Location': [], 'Sentiment': []})
    statesdf = pd.DataFrame({'Location': [], 'Sentiment': []})
    df.drop(columns=['id','location', 'text',])
    df = df[0:2000]
    for i in tqdm(range(len(df))):
        if isinstance(df.clean_location.iloc[i], str):
            countriesdf = countriesdf.append({'Date': df.date.iloc[i], 'Location': df.clean_location.iloc[i], 'Sentiment': df.sentiment_score.iloc[i]},ignore_index=True)
        elif isinstance(df.clean_location.iloc[i], list):
            statesdf = statesdf.append({'Date': df.date.iloc[i], 'Location': df.clean_location.iloc[i][3], 'Sentiment': df.sentiment_score.iloc[i]},ignore_index=True)


    statesdf.to_pickle('statesdf.pkl')
    countriesdf.to_pickle('countriesdf.pkl')


# splitDf()
# plotGlobalSentiments('states')
