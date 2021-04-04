import pandas as pd
import numpy as np
import geonamescache
import re
import us
from city_to_state import city_to_state_dict
from country_to_code import country_to_code_dict
from pprint import pprint
import pickle as pck


gc = geonamescache.GeonamesCache()

def find_country(text):
    for k,v in country_to_code_dict.items():
        if re.search(k,  text, re.IGNORECASE):
            return [k,v[0]]
        # elif re.search(v[0],  text, re.IGNORECASE):
        #     return [k,v[0]]
        # elif re.search(v[1],  text, re.IGNORECASE):
        #     return [k,v[0]]

def find_country_from_city(text):
    with open('city_to_country.pck', 'rb') as f:
        city_to_country_dict = pck.load(f)
    for k,v in city_to_country_dict.items():
        if re.search(k,  text, re.IGNORECASE):
            if v == 'US':
                return find_state(text)
            for countryKey, countryCodes in country_to_code_dict.items():
                if re.search(countryCodes[1],  v, re.IGNORECASE):
                    return [k,countryCodes[0]]



def find_state(text):
    states = gc.get_us_states()
    state_names = [i[1]['name'] for i in states.items()]
    for pattern in state_names:
        if re.search(pattern,  text, re.IGNORECASE):
            return ['United States', 'USA', pattern,  us.states.lookup(str(pattern)).abbr]
    if re.match('({})'.format("|".join(city_to_state_dict.keys()).lower()), text.lower()):
        k = re.match('({})'.format("|".join(city_to_state_dict.keys()).lower()), text.lower()).group(0)
        tokens = [city_to_state_dict.get(k.title(), np.nan)]
    else:
        tokens = [j for j in re.split("\s|,", text) if j not in ['in', 'la', 'me', 'oh', 'or']]
    for i in tokens:
        if re.match('\w+', str(i)):
            if us.states.lookup(str(i)):
                return ['United States', 'USA', i,  us.states.lookup(str(i)).abbr]

def clean_location(x):
    country = find_country(str(x))
    state = find_state(str(x))
    # countryFromCity = find_country_from_city(str(x))
    if country:
        return country
    elif state:
        return state
    else:
        return find_country_from_city(str(x))

