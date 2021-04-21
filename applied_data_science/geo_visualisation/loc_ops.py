import pandas as pd
import numpy as np
import geonamescache
from re import search, IGNORECASE, split, match
from us.states import lookup 
from .city_to_state import city_to_state_dict
from .country_to_code import country_to_code_dict
from pprint import pprint
import pickle as pck


gc = geonamescache.GeonamesCache()

# with open('city_to_country.pck', 'rb') as f:
#     city_to_country_dict = pck.load(f)

state_names = [i[1]['name'] for i in gc.get_us_states().items()]

city_to_state_pattern = '({})'.format("|".join(city_to_state_dict.keys()).lower())


def find_country(text):
    for k,v in country_to_code_dict.items():
        if  search(k,  text,  IGNORECASE):
            return v[0]
        # elif  search(v[0],  text,  IGNORECASE):
        #     return [k,v[0]]
        # elif  search(v[1],  text,  IGNORECASE):
        #     return [k,v[0]]

def find_country_from_city(text):
    for k,v in city_to_country_dict.items():
        if  search(k,  text,  IGNORECASE):
            # if v == 'US':
            #     return find_state(text)
            for countryKey, countryCodes in country_to_code_dict.items():
                if  search(countryCodes[1],  v,  IGNORECASE):
                    return countryCodes[0]

def find_state(text):

    for pattern in state_names:
        if  search(pattern,  text,  IGNORECASE):
            return ['United States', 'USA', pattern,  lookup(str(pattern)).abbr]

    matches = match(city_to_state_pattern, text.lower())
    if matches:
        k =  matches.group(0)
        tokens = [city_to_state_dict.get(k.title(), np.nan)]
    else:
        tokens = [j for j in  split("\s|,", text) if j not in ['in', 'la', 'me', 'oh', 'or']]

    for i in tokens:
        if  match('\w+', str(i)):
            if lookup(str(i)):
                return ['United States', 'USA', i,  lookup(str(i)).abbr]

def clean_location(x):
    if not x:
        return None
        
    state = find_state(str(x))
    if not state:
        country = find_country(str(x))

    # countryFromCity = find_country_from_city(str(x))
    if state:
        return state
    elif country:
        return country
    else:
        return None
    # else:
    #     return find_country_from_city(str(x))

