import requests
import os
import json

from pathlib import Path
from datetime import datetime

standard_filters = 'lang:en -is:retweet'

rules = [
    {"value": "(vaccine OR jab)" + " " + standard_filters, "tag": "vaccines"},
    {"value": "(AZ OR astra-zeneca OR astrazeneca)" + " " + standard_filters, "tag": "az-vaccine"},
    {"value": "(phizer OR biontech)" + " " + standard_filters, "tag": "pb-vaccine"},
    {"value": "moderna" + " " + standard_filters, "tag": "m-vaccine"},
]

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_rules(headers):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print('Get Rules:')
    print(json.dumps(response.json()))
    return response.json()


def clear_rules(headers):

    rules = get_rules(headers)

    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print('Clear Rules:')
    print(json.dumps(response.json()))


def add_rules(headers, rules):
    # You can adjust the rules if needed
    payload = {"add": rules, 'dry_run': True}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print('Add Rules:')
    print(json.dumps(response.json()))



def main():
    bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')

    headers = create_headers(bearer_token)

    clear_rules(headers)
    add_rules(headers, rules)



__name__ == '__main__' and main()

