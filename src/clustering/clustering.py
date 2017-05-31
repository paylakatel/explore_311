import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Point
import pysal as ps


def clean_data(df):
    df = df.copy()
    # filter for only closed cases
    df = df.loc[df['CASE_STATUS'] == 'Closed']

    # drop points geocoded to city hall ~100,000 of them in the data set
    odd = df.loc[(df.Latitude == 42.3594) & (df.Longitude == -71.0587), ['Longitude', 'Latitude']]
    df = df.drop(odd.index)

    # convert open and closed fields to datetimes
    df.loc[:, 'open_dt'] = pd.to_datetime(df['open_dt'], format="%Y-%m-%d %H:%M:%S")
    df.loc[:, 'closed_dt'] = pd.to_datetime(df['closed_dt'], format="%Y-%m-%d %H:%M:%S")

    # calculate open length
    df.loc[:, 'open_len'] = df['closed_dt'] - df['open_dt']
    df.loc[:, 'open_len'] = df['open_len'].astype('timedelta64[h]')
    return df


def convert_to_gpd_df(df):
    geometry = [Point(xy) for xy in zip(df.Longitude, df.Latitude)]
    df = df.drop(['Longitude', 'Latitude'], axis=1)
    crs = {'init': 'epsg:4326'}
    return GeoDataFrame(df, crs=crs, geometry=geometry)


def join_311_to_blocks(gdf, blocks):
    df_blocks = gpd.sjoin(blocks, gdf, how="inner", op='intersects')
    df_blocks["count"] = 1
    df_blocks = df_blocks[['BG_ID', 'open_len', 'count', 'geometry']]
    return df_blocks


def get_queen_neighbors_matrix(df, outfile):
    df.to_file(outfile, driver='ESRI Shapefile')
    weights = ps.queen_from_shapefile(outfile, idVariable='BG_ID')
    weights.transform = 'r'
    return weights







