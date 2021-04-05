import pandas as pd
import pandas_gbq as pdbq

from datetime import date
from google.oauth2 import service_account

PROJECT_ID = "ads-coursework-308518"

DEFAULT_FIELDS = ["id", "author_location", "text", "created_at"]


def get_filtered_stream_tweets(start_date, end_date, fields=DEFAULT_FIELDS):

    if not (start_date >= date(2021, 3, 23) and end_date <= date.today()):
        raise ValueError("Invalid start date")

    credentials = service_account.Credentials.from_service_account_file(
        "./BigQuery-SA.json",
    )

    query = f"""
    select
      {','.join(fields)}
    from `Tweets.filtered_vaccine_tweets_nobots`
    where
        EXTRACT(DATE from created_at) >= DATE({start_date.year}, {start_date.month}, {start_date.day})
      AND
        EXTRACT(DATE from created_at) <= DATE({end_date.year}, {end_date.month}, {end_date.day})
    """

    df = pdbq.read_gbq(query, project_id=PROJECT_ID, credentials=credentials)
    return df


def get_general_covid_tweets(start_date, end_date, fields=DEFAULT_FIELDS):

    if not (start_date <= date(2020, 1, 20) and end_date <= date(2021, 3, 28)):
        raise ValueError("Invalid start date")

    credentials = service_account.Credentials.from_service_account_file(
        "./BigQuery-SA.json",
    )

    query = f"""
    select
      {','.join(fields)}
    from `Tweets.covidtweets`
    where
        EXTRACT(DATE from created_at) >= DATE({start_date.year}, {start_date.month}, {start_date.day})
      AND
        EXTRACT(DATE from created_at) <= DATE({end_date.year}, {end_date.month}, {end_date.day})
    """

    df = pdbq.read_gbq(query, project_id=PROJECT_ID, credentials=credentials)
    return df
