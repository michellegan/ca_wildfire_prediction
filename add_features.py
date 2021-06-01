import pandas as pd
import sys
import datetime

#script to generate dataset linking countydate-> population density
CA_WILDFIRES = "./misc/fire_incidents.csv"

wildfire_data = pd.read_csv (CA_WILDFIRES, sep=",", header=0)
 

