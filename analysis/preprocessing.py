from clustering.clustering import clean_data, convert_to_gpd_df, join_311_to_blocks, get_queen_neighbors_matrix
import pandas as pd
import seaborn as sns
import geopandas as gpd
import pysal as ps

csv = "./data/311.csv"
encoding = "ISO-8859-1"
cols = ["CASE_ENQUIRY_ID", "open_dt", "closed_dt", "CASE_STATUS", "Latitude", "Longitude"]

df = pd.read_csv(csv, encoding=encoding, usecols=cols)

# clean up dataframe
df = clean_data(df)

# plot lat/long
#sns.jointplot(x="Longitude", y="Latitude", data=df)
#sns.plt.show()

# convert to geopandas df
gdf = convert_to_gpd_df(df)

# load census blocks
blocks = gpd.read_file('./data/census2000blockgroups_poly/census2000blockgroups_poly.shp')
blocks = blocks.loc[blocks['COUNTY'] == '025']
blocks = blocks.to_crs({'init': 'epsg:4326'})

df_blocks = join_311_to_blocks(gdf, blocks)

# create neighbors from file
outfile = "./data/tmp/tmp.shp"
weight_matrix = get_queen_neighbors_matrix(gdf, outfile)

# create quanitiles for open len
open_len_Q10 = ps.Quantiles(gdf.open_len, k=10)
print(type(open_len_Q10))
print(open_len_Q10)

