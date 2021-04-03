# -*- coding: utf-8 -*-
import requests
import os
import json

from pathlib import Path
from datetime import datetime, timedelta


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_stream(headers, limit, time_to_break):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?expansions=author_id,geo.place_id,referenced_tweets.id"
        "&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type"
        "&tweet.fields=context_annotations,author_id,entities,geo,id,public_metrics,possibly_sensitive,text,withheld,created_at"
        "&user.fields=entities,id,location,name,verified,description", headers=headers, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    tweets = []
    for response_line in response.iter_lines():
        if datetime.now() > time_to_break:
            return tweets
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))
            tweets.append(json_response)
            if len(tweets) > limit:
                return tweets
    return tweets


def main():
    invokation_time = datetime.now()
    # Max 11 tweets per minute
    limit = int(os.environ.get('LIMIT'))
    bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')
    results_folder = Path('./results')

    headers = create_headers(bearer_token)

    tweets = get_stream(headers, limit, invokation_time + timedelta(minutes=4.5))


    filename = invokation_time.strftime("%Y-%m-%d--%H-%M.json")
    with (results_folder / filename).open('w') as f:
        f.write(json.dumps(tweets))

__name__ == '__main__' and main()

