from clustering.clustering import clean_data, convert_to_gpd_df, join_311_to_blocks, get_queen_neighbors_matrix
import pandas as pd
import seaborn as sns
import geopandas as gpd
import pysal as ps

csv = "../data/311.csv"
encoding = "ISO-8859-1"
cols = ["CASE_ENQUIRY_ID", "open_dt", "closed_dt", "CASE_STATUS", "Latitude", "Longitude"]

df = pd.read_csv(csv, encoding=encoding, usecols=cols)

# clean up dataframe
df = clean_data(df)

# plot lat/long in jointplot
sns.jointplot(x="Longitude", y="Latitude", data=df)
sns.plt.show()
# save jointplot to csv
jointplot = df[['Latitude', 'Longitude']]
jointplot.to_csv("../data/web/jointplot.csv")

# convert to geopandas df
gdf = convert_to_gpd_df(df)

# load census blocks
blocks = gpd.read_file('../data/census2000blockgroups_poly/census2000blockgroups_poly.shp')
blocks = blocks.loc[blocks['COUNTY'] == '025']
blocks = blocks.to_crs({'init': 'epsg:4326'})

df_blocks = join_311_to_blocks(gdf, blocks)

# create neighbors from file
outfile = "../data/tmp/tmp.shp"
weight_matrix = get_queen_neighbors_matrix(gdf, outfile)

# create natural breaks for open len
open_len_FJ10 = ps.Fisher_Jenks(df_blocks.open_len, k=10)
print("Fisher Jenks breaks - open len: {}".format(open_len_FJ10))
print("Fisher Jenks fit- open len: {}".format(open_len_FJ10.adcm))
# join breaks back to blocks df
df_blocks = df_blocks.assign(open_len_cl=open_len_FJ10.yb)

# calculate spatial lag
open_len_lag = ps.lag_spatial(weight_matrix, df_blocks.open_len.values)
open_len_lag_FJ10 = ps.Fisher_Jenks(open_len_lag, k=10)
print("Fisher Jenks breaks - open len lag: {}".format(open_len_lag_FJ10))
print("Fisher Jenks fit - open len lag: {}".format(open_len_lag_FJ10.adcm))
# join lag breaks back to blocks
df_blocks = df_blocks.assign(open_len_lag_cl=open_len_lag_FJ10.yb)

df_blocks.to_csv("../data/web/df_block.csv")

