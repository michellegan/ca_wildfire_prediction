import pandas as pd

CENSUS_API = "api.census.gov/data/2019/pep/population?get=COUNTY,DENSITY,POP,NAME,STATE&for=state:06&key=" + CENSUS_API_KEY
CA_WILDFIRES = '../fire_incidents.csv'

wildfire_data = pd.read_csv(CA_WILDFIRES, sep=",", header=0)

counties = wildfire_data['Counties'].tolist()

for county in counties: