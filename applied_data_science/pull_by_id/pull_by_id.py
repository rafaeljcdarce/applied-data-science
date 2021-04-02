import requests
import json
import random
import csv
import time


expansions = "author_id,geo.place_id,referenced_tweets.id"
placefields   = "contained_within,country,country_code,full_name,geo,id,name,place_type"
tweetfields = "context_annotations,author_id,entities,geo,id,public_metrics,possibly_sensitive,text,withheld,created_at"
userfields =  "entities,id,location,name,verified,description"
fields = f"expansions={expansions}&place.fields={placefields}&tweet.fields={tweetfields}&user.fields={userfields}"

bearertoken = None # Change this to your token


def ids_from_file(filename):
    with open(filename,'r') as f:
        reader = csv.reader(f,delimiter="\t")
        next(reader) #header lines
        ids = [line[0] for line in reader]
    return ids

def lines_if_en(filename):
    with open(filename,'r') as f:
        reader = csv.reader(f,delimiter="\t")
        next(reader) #header lines
        ids = [line for line in reader if line[3] == "en"]
    return ids



def tweets_by_id(ids):
    assert(len(ids) <= 100)
    ids = ",".join(ids)
    response = requests.get(f"https://api.twitter.com/2/tweets?ids={ids}&{fields}",headers={"Authorization" : f"Bearer {bearertoken}"})
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get data (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    remaining = int(response.headers["x-rate-limit-remaining"])
    reset = int(response.headers["x-rate-limit-reset"])
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            tweets = json_response
            return tweets,remaining,reset


def soa2aos(tweets):
    aos = []
    for i in range(len(tweets["data"])):
        includeobj = {"users":[tweets["includes"]["users"][i]]}
        item = {"data" : tweets["data"][i], "includes" : includeobj}
        aos.append(item)
    return aos

def main():
    ids = ids_from_file("2020-03-22_clean-dataset.tsv")
    ids = random.choices(ids,k=100)
    tweets = None
    remaining = 1
    for i in range(0,len(ids),100):
        if remaining == 0:
            print(f"Hit rate limit, sleeping for {reset-time.time()} seconds")
            time.sleep(reset-time.time())
        try:
            newtweets, remaining, reset = tweets_by_id(ids[i:i+100])
            print(remaining,reset)
            if tweets == None:
                tweets = newtweets
            else:
                tweets["data"].extend(newtweets["data"])
                for key in newtweets["includes"].keys():
                    tweets["includes"][key].extend(newtweets["includes"][key])

        except:
            continue
        
    tweets = soa2aos(tweets)
    with open("results.json",'w') as f:
        f.write(json.dumps(tweets))

if __name__ == '__main__':
    main()
    