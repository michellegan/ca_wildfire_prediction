import pandas as pd
import sys
import datetime, calendar
from datetime import date, timedelta


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
wildfire_data['County'] = wildfire_data['Counties']

#get the subset of columns that we care about for each wildfire - # of acres burned, the counties involved in the fire, lat and long of fire start, date fire started
#these columns will help us generate the other features
wildfire_data = wildfire_data[['AcresBurned', 'County','Latitude', 'Longitude', 'Date']] 

#take out irrelevant counties
wildfire_data = wildfire_data[wildfire_data.County != 'State of Oregon']
wildfire_data = wildfire_data[wildfire_data.County != 'State of Nevada']

#prepare dataframe
columns = ['county', 'date', 'fire_occurrence', 'acres_burned']
d = {}

counties = set(wildfire_data['County'].tolist())
for county in list(counties):
    sdate = datetime.datetime.strptime('2013-01-01', "%Y-%m-%d")
    edate = datetime.datetime.strptime('2020-01-01', "%Y-%m-%d")
    dates = [sdate+timedelta(days=x) for x in range((edate-sdate).days)]
    for day in dates:
        day_string = day.strftime("%Y-%m-%d")
        def get_acres_burned (county, day_string):
            subset = wildfire_data[(wildfire_data['Date'] == day_string) & (wildfire_data['County'] == county)]
            
            if len(subset) == 0:
                return 0
            else:
                try:
                    acres_burned = str(subset['AcresBurned'].to_string(index=False).strip('\n'))
                    if '\n' in acres_burned:
                        acres = acres_burned.split('\n')
                        cleaned_acres = []
                        for x in acres:
                            new = int(float(x.strip()))
                            cleaned_acres.append(new)
                        acres_burned = sum(cleaned_acres)
                    else:
                        acres_burned = int(float((acres_burned.strip())))
                except:
                    acres_burned = 0
                return acres_burned
        acres_burned = get_acres_burned(county, day_string)
        if acres_burned != 0:
            output = 1
        else:
            output = 0
        to_add = [county, day_string, output, acres_burned]
        d[(county, day_string)] = to_add
df = pd.DataFrame.from_dict(d, orient='index', columns=columns)
df = df[columns]
df.to_csv ('all_data.csv', index=False, columns=columns, header=columns)


