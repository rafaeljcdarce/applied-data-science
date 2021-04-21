import pandas as pd
import pandas_gbq as pdbq

from datetime import date
from google.oauth2 import service_account

PROJECT_ID = "ads-coursework-308518"

DEFAULT_FIELDS = ["id", "author_location", "text", "created_at"]



def get_filtered_stream_tweets(start_date, end_date, fields=DEFAULT_FIELDS):
    query = f"""
    select
      {','.join(fields)}
    from `Tweets.filtered_vaccine_tweets`
    where
        EXTRACT(DATE from created_at) >= DATE({start_date.year}, {start_date.month}, {start_date.day})
      AND
        EXTRACT(DATE from created_at) <= DATE({end_date.year}, {end_date.month}, {end_date.day})
    """

    return data_helper(start_date, date(2021, 3, 23), end_date, date.today(), query, fields)


def get_vaccine_tweets(start_date, end_date, fields=DEFAULT_FIELDS):
    query = f"""
    select
      {','.join(fields)}
    from `Tweets.covidtweets2`
    where
        EXTRACT(DATE from created_at) >= DATE({start_date.year}, {start_date.month}, {start_date.day})
      AND
        EXTRACT(DATE from created_at) <= DATE({end_date.year}, {end_date.month}, {end_date.day})
    """

    return data_helper(start_date, date(2020, 10, 2), end_date, date(2021, 3, 28), query, fields)


def get_general_covid_tweets(start_date, end_date, fields=DEFAULT_FIELDS):
    query = f"""
    select
      {','.join(fields)}
    from `Tweets.covidtweets`
    where
        EXTRACT(DATE from created_at) >= DATE({start_date.year}, {start_date.month}, {start_date.day})
      AND
        EXTRACT(DATE from created_at) <= DATE({end_date.year}, {end_date.month}, {end_date.day})
    """

    return data_helper(start_date, date(2020, 1, 20), end_date, date(2021, 3, 28), query, fields)

def data_helper(start_date, valid_start_date, end_date, valid_end_date, query, fields):
    if not (start_date <= valid_start_date and end_date <= valid_end_date):
        raise ValueError("Invalid start date")

    credentials = service_account.Credentials.from_service_account_file(
        "./BigQuery-SA.json",
    )

    df = pdbq.read_gbq(query, project_id=PROJECT_ID, credentials=credentials)
    return df
    
