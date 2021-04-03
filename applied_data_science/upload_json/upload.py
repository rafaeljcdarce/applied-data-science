# -*- coding: utf-8 -*-

import argparse
import json
import pandas as pd
import pandas_gbq as pdbq

from google.oauth2 import service_account
from datetime import datetime

PROJECT_ID = 'ads-coursework-308518'


def jsonfile_to_df(path, matched_rules=False):
    with open(path, 'r') as f:
        data = json.loads(f.read())

    return data_to_df(data, matched_rules)

def data_to_df(data, matched_rules=False):
    labels = [
        'id',
        'author_id',
        'author_handle',
        'author_name',
        'author_description',
        'author_location',
        'author_verified',
        'text',
        'is_reply',
        'like_count',
        'quote_count',
        'reply_count',
        'retweet_count',
        'created_at',
    ]

    matched_rules and labels.append('matched_rules')

    formatted_data = []
    _fd_append = formatted_data.append
    for record in data:
        r = extract_record(record)
        if not matched_rules:
            del r['matched_rules']
        _fd_append(r)

    df = pd.DataFrame(data=formatted_data, columns=labels)
    return df

def extract_record(record):
    data = record['data']
    includes = record['includes']
    matched_rules = record['matching_rules'] if 'matching_rules' in record else []
    metrics = data['public_metrics']

    author_id = data['author_id']
    author = None
    for user in includes['users']:
        if user['id'] == author_id:
            author = user
            break

    rules = ','.join([rule['tag'] for rule in matched_rules])
    return {
        'id': data['id'],
        'author_id': author['id'],
        'author_handle': author['username'],
        'author_name': author['name'],
        'author_description': author['description'].replace('\r', '') if 'description' in author else None,
        'author_location': author['location'] if 'location' in author else None,
        'author_verified': author['verified'],
        'text': data['text'].replace('\r', ''),
        'is_reply': 'referenced_tweets' in data,
        'like_count': metrics['like_count'],
        'quote_count': metrics['quote_count'],
        'reply_count': metrics['reply_count'],
        'retweet_count': metrics['retweet_count'],
        'created_at': datetime.fromisoformat(data['created_at'][:-1]),
        'matched_rules': rules,
    }

def upload_df(creds, df, table_name):
   pdbq.to_gbq(
       df, f'Tweets.{table_name}', project_id=PROJECT_ID, if_exists='append', credentials=creds
   )

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    parser = argparse.ArgumentParser('upload json to BigQuery')

    parser.add_argument('Path', metavar='path', type=str,
                        help='the path to json file to upload')
    parser.add_argument('table_name', type=str,
                        help='table to upload to')
    parser.add_argument("--matched_rules", type=str2bool, nargs='?',
                            const=True, default=False,
                            help="Add matched rules")

    args = parser.parse_args()

    credentials = service_account.Credentials.from_service_account_file(
        './service-account.json',
    )
    df = jsonfile_to_df(args.Path, args.matched_rules)

    upload_df(credentials, df, args.table_name)

__name__ == '__main__' and main()
