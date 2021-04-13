import plotly.express as px
import pandas as pd 
import numpy as np
from pprint import pprint
from geocleaner import clean_locations

def plotGlobalSentiments(df, mode):
    # df = df.drop(df.columns[[0]], axis=1) 
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
        'Locations': countries,
        'Sentiment': sentiments
    })
    if mode == 'countries':
        fig = px.choropleth(countrySentimentsdf, locations="Locations",
                            color="Sentiment", # lifeExp is a column of gapminder
                            # hover_name="country", # column to add to hover information
                            color_continuous_scale=px.colors.sequential.Plasma)
    elif mode == 'states':
        print(countrySentimentsdf['Locations'])
        fig = px.choropleth(countrySentimentsdf,  # Input Pandas DataFrame
                    locations="Locations",  # DataFrame column with locations
                    color="Sentiment",  # DataFrame column with color values
                    # hover_name="state", # DataFrame column hover info
                    locationmode = 'USA-states', color_continuous_scale=px.colors.sequential.Plasma)

        fig.update_layout(
            title_text = 'Geographical Distribution of', # Create a Title
            geo_scope='usa',  # Plot only the USA instead of globe
        )
    # fig.show()
    fig.write_image("images/"+mode+"Sentiments.pdf")



# cleaned_locs = clean_locations()
df = pd.read_pickle('locateddf.pkl')
countriesdf = pd.DataFrame({'Location': [], 'Sentiment': []})
statesdf = pd.DataFrame({'Location': [], 'Sentiment': []})
for i in range(len(df)):
    if isinstance(df.Location.iloc[i], str):
        countriesdf.loc[i] = list(df.iloc[i])
    elif isinstance(df.Location.iloc[i], list):
        statesdf.loc[i] = list([df.iloc[i][0][3],df.iloc[i][1]])
print(countriesdf)
print(statesdf)
# fig = px.choropleth()
plotGlobalSentiments(countriesdf, 'countries')
plotGlobalSentiments(statesdf, 'states')
