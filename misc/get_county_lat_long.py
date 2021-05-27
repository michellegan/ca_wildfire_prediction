import pandas as pd
import sys


LAT_LONG = "./us-county-boundaries.csv"
columns=['county_name', 'latitude', 'longitude']

lat_long = pd.read_csv (LAT_LONG, sep=";", header=0)
ca_data = lat_long[lat_long.STATE_NAME == 'California']
ca_data = ca_data[['NAME','INTPTLAT','INTPTLON']]
ca_data.to_csv ('county_lat_long.csv', index=False, header=columns)