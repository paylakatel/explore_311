import requests
import pandas as pd
from pandas.io.json import json_normalize


def get_data(url, key1=None, key2=None):
    r = requests.get(url)
    data = r.json().get(key1).get(key2)
    return json_normalize(data)





