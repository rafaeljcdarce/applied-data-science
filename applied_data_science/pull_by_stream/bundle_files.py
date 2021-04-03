# -*- coding: utf-8 -*-
import os
import json

from datetime import timedelta, date

def main():

    yesterday = date.today() - timedelta(days=1)

    files = os.listdir('results/')

    files_yesterday = filter(lambda f: yesterday.strftime('%Y-%m-%d--') in f, files)

    data = []
    for fy in files_yesterday:
        print(fy)
        with open(f'results/{fy}', 'r') as f:
            data += json.loads(f.read())

    with open(yesterday.strftime('results/%Y-%m-%d.json'), 'w') as f:
        f.write(json.dumps(data))


__name__ == '__main__' and main()
