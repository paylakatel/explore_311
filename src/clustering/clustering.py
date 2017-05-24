import requests
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib


def get_data(url, key1=None, key2=None):
    r = requests.get(url)
    data = r.json().get(key1).get(key2)
    return json_normalize(data)


def clean_data(df):
    df = df.loc[df['CASE_STATUS'] == 'Closed']
    df = df.filter(['CASE_ENQUIRY_ID',
                    'Department',
                    'Latitude',
                    'Longitude',
                    'QUEUE',
                    'TYPE',
                    'open_dt',
                    'closed_dt',
                    'target_dt'], axis=1)
    df['open_dt'] = pd.to_datetime(df['open_dt'], format="%Y-%m-%d %H:%M:%S")
    df['closed_dt'] = pd.to_datetime(df['closed_dt'], format="%Y-%m-%d %H:%M:%S")
    return df


def calculate_open_length(df, open_dt, closed_dt):
    df['open_len'] = df['closed_dt'] - df['open_dt']
    df['open_len'] = df['open_len'].astype('timedelta64[h]')






