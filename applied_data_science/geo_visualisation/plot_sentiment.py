import plotly.express as px
import pandas as pd 
import numpy as np
from pprint import pprint

def plot_sentiments(locationdatafile):
    df = pd.read_csv(locationdatafile)
    unique_locations = df.Location.unique()


    all_sentiments = {}
    for location, sentiment in zip(df['Location'], df['Sentiment']):
        try:
            all_sentiments[location].append(sentiment)
        except:
            all_sentiments[location] = [sentiment]

    # pprint(all_sentiments)
    countries = []
    sentiments = []
    for country, sentiment in all_sentiments.items():
        average_sentiment = np.average(sentiment)
        countries.append(country)
        sentiments.append(average_sentiment)
        # print(countrySentimentsdf[location])

    countrySentimentsdf = pd.DataFrame({
        'Countries': countries,
        'Sentiments': sentiments
    })

    fig = px.choropleth(countrySentimentsdf, locations="Countries",
                        color="Sentiments", # lifeExp is a column of gapminder
                        # hover_name="country", # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Plasma)
    fig.show()

plot_sentiments('locatedData.csv')