import pandas as pd
import sys
import datetime

CA_WILDFIRES = "./California_Fire_Incidents.csv"

wildfire_data = pd.read_csv (CA_WILDFIRES, sep=",", header=0)

#reformat the date so that it is in YYYY-MM-DD format
def get_date(x):
    try:
        d = datetime.datetime.strptime(x,"%Y-%m-%dT%H:%M:%SZ")
    except:
        d = datetime.datetime.strptime("2013-07-10T11:00:00.000Z","%Y-%m-%dT%H:%M:%S.%fZ")
    return d.strftime ("%Y-%m-%d")

wildfire_data['Date'] = wildfire_data['Started'].apply(lambda x: get_date(x)) 

#get the subset of columns that we care about for each wildfire - # of acres burned, the counties involved in the fire, lat and long of fire start, date fire started
#these columns will help us generate the other features
wildfire_data = wildfire_data[['AcresBurned', 'Counties','Latitude', 'Longitude', 'Date']] 

wildfire_data.to_csv('fire_incidents.csv', index=False, sep=",", header = ['AcresBurned', 'Counties','Latitude', 'Longitude', 'Date'])