import pandas as pd
import sys
import datetime, calendar
from datetime import date, timedelta
from statistics import mean
import math
from decimal import Decimal


#script to generate dataset linking countydate-> population density
all_data = "./all_data.csv"
all_data = pd.read_csv(all_data, sep=",", header=0)

county_paths_dict = {
    "alameda": "./county_temperatures/A-L Counties/Alameda.csv",
    "butte": "./county_temperatures/A-L Counties/Butte.csv",
    "contra costa": "./county_temperatures/A-L Counties/Contra Costa.csv",
    "del norte": "./county_temperatures/A-L Counties/Del Norte.csv",
    "el dorado": "./county_temperatures/A-L Counties/El Dorado.csv",
    "fresno": "./county_temperatures/A-L Counties/Fresno.csv",
    "humboldt": "./county_temperatures/A-L Counties/Humboldt.csv",
    "inyo": "./county_temperatures/A-L Counties/Inyo.csv",
    "kern": "./county_temperatures/A-L Counties/Kern.csv",
    "kings": "./county_temperatures/A-L Counties/Kings.csv",
    "los angeles": "./county_temperatures/A-L Counties/Los Angeles.csv",
    "madera": "./county_temperatures/M-R/Madera.csv",
    "marin": "./county_temperatures/M-R/Marin.csv",
    "mariposa": "./county_temperatures/M-R/Mariposa.csv",
    "mendocino": "./county_temperatures/M-R/Mendocino.csv",
    "merced": "./county_temperatures/M-R/Merced.csv",
    "modoc": "./county_temperatures/M-R/Modoc.csv",
    "mono": "./county_temperatures/M-R/Mono.csv",
    "monterey": "./county_temperatures/M-R/Monterey.csv",
    "napa": "./county_temperatures/M-R/Napa.csv",
    "nevada": "./county_temperatures/M-R/Nevada.csv",
    "orange": "./county_temperatures/M-R/Orange.csv",
    "placer": "./county_temperatures/M-R/Placer.csv",
    "riverside": "./county_temperatures/M-R/Riverside.csv",
    "sacramento": "./county_temperatures/Sacramento-Siskiyou/Sacramento.csv",
    "san benito": "./county_temperatures/Sacramento-Siskiyou/San Benito.csv",
    "san bernardino": "./county_temperatures/Sacramento-Siskiyou/San Bernardino.csv",
    "san diego": "./county_temperatures/Sacramento-Siskiyou/San Diego.csv",
    "san joaquin": "./county_temperatures/Sacramento-Siskiyou/San Joaquin.csv",
    "san luis obispo": "./county_temperatures/Sacramento-Siskiyou/San Luis Obispo.csv",
    "san mateo": "./county_temperatures/Sacramento-Siskiyou/San Mateo.csv",
    "santa barbara": "./county_temperatures/Sacramento-Siskiyou/Santa Barbara.csv",
    "santa clara": "./county_temperatures/Sacramento-Siskiyou/Santa Clara.csv",
    "santa cruz": "./county_temperatures/Sacramento-Siskiyou/Santa Cruz.csv",
    "shasta": "./county_temperatures/Sacramento-Siskiyou/Shasta.csv",
    "siskiyou": "./county_temperatures/Sacramento-Siskiyou/Siskiyou.csv",
    "solano": "./county_temperatures/Solano-Yuba/Solano.csv",
    "sonoma": "./county_temperatures/Solano-Yuba/Sonoma.csv",
    "stanislaus": "./county_temperatures/Solano-Yuba/Stanislaus.csv",
    "tehama": "./county_temperatures/Solano-Yuba/Tehama.csv",
    "trinity": "./county_temperatures/Solano-Yuba/Trinity.csv",
    "tulare": "./county_temperatures/Solano-Yuba/Tulare.csv",
    "tuolumne": "./county_temperatures/Solano-Yuba/Tuolumne.csv",
    "ventura": "./county_temperatures/Solano-Yuba/Ventura.csv",
    "yolo": "./county_temperatures/Solano-Yuba/Yolo.csv",
    "yuba": "./county_temperatures/Solano-Yuba/Yuba.csv"
}

all_data['county'] = all_data['county']
all_data['dates'] = all_data['date']
all_data['fire_occurence'] = all_data['fire_occurrence']
all_data['acres_burned'] = all_data['acres_burned']

all_data = all_data[['county', 'date','fire_occurrence', 'acres_burned']] 

counties_inc = ["Alameda", "Butte", "Contra Costa", "Del Norte", "El Dorado", "Fresno", "Humboldt", "Inyo", "Kern", "Kings", "Los Angeles", "Madera", "Marin", "Mariposa", "Mendocino", "Merced", "Modoc", "Mono", "Monterey", "Napa", "Nevada", "Orange", "Placer", "Riverside", "Sacramento", "San Benito", "San Bernardino", "San Diego", "San Joaquin", "San Luis Obispo", "San Mateo", "Santa Barbara", "Santa Clara", "Santa Cruz", "Shasta", "Siskiyou", "Solano", "Sonoma", "Stanislaus", "Tehama", "Trinity", "Tulare", "Tuolumne", "Ventura", "Yolo", "Yuba"]

all_data = all_data[all_data['county'].isin(counties_inc)]


#prepare dataframe
columns = ['county', 'date', 'fire_occurrence', 'acres_burned', "avg_dp_temp", "avg_rel_hum", "avg_wb_temp", "avg_wind_speed", "precip", "pop_density", "latitude", "longitude"]
d = {}

counties = set(all_data['county'].tolist())

dates = all_data['date']

pop_density_df = pd.read_csv("./county_pop_density.csv")
lat_long = pd.read_csv("./county_lat_long.csv")


for county in list(counties):
    print("county", county)
    formatted_county = (county.lower())
    curr_county_file = pd.read_csv(county_paths_dict[formatted_county], sep=",", header=0)

    date_col = curr_county_file["DATE"]
    avg_dp_temp_col = curr_county_file["DailyAverageDewPointTemperature"]
    avg_db_temp_col = curr_county_file["DailyAverageDryBulbTemperature"]
    avg_rel_hum_col = curr_county_file["DailyAverageRelativeHumidity"]
    avg_wb_temp_col = curr_county_file["DailyAverageWetBulbTemperature"]
    avg_wind_speed_col = curr_county_file["DailyAverageWindSpeed"]
    precip_col = curr_county_file["DailyPrecipitation"]

    all_data_sub_df = all_data[all_data['county'] == county]
    fire_occ_curr = mean(all_data_sub_df['fire_occurrence'])
    acres_burned_curr = mean(all_data_sub_df['acres_burned'])

    curr_lat = lat_long[lat_long['county_name'] == county]['latitude'].item()
    print(curr_lat)
    curr_long = lat_long[lat_long['county_name'] == county]['longitude'].item()
    print(curr_long)
    curr_pop_density = pop_density_df[pop_density_df['county_n'] == county][' pop_density'].item()
    print(curr_pop_density)

    county_file_length = curr_county_file.shape[0]
    all_data_length = all_data.shape[0]

    first_date = curr_county_file['DATE'][0]
    second_date = first_date.replace('-01-01', '-01-02')

    first_index = curr_county_file.index[curr_county_file['DATE'] == first_date].tolist()
    second_index = curr_county_file.index[curr_county_file['DATE'] == second_date].tolist()
    gap = int(second_index[0] - first_index[0])


    for i in range(0, county_file_length, gap):
        curr_date = date_col[i]

        sub_county_df = curr_county_file[curr_county_file['DATE'] == curr_date]

        sub_county_df["HourlyDewPointTemperature"] = (
            pd.to_numeric(sub_county_df["HourlyDewPointTemperature"],
                  errors='coerce')
                    .fillna(0)
            )

        sub_county_df["HourlyWetBulbTemperature"] = (
            pd.to_numeric(sub_county_df["HourlyWetBulbTemperature"],
                  errors='coerce')
                    .fillna(0)
            )

        
        sub_county_df["HourlyWindSpeed"] = (
            pd.to_numeric(sub_county_df["HourlyWindSpeed"],
                  errors='coerce')
                    .fillna(0)
            )

        sub_county_df["HourlyRelativeHumidity"] = (
            pd.to_numeric(sub_county_df["HourlyRelativeHumidity"],
                  errors='coerce')
                    .fillna(0)
            )

        avg_dp_temp = mean(sub_county_df["HourlyDewPointTemperature"])
        avg_rel_hum = mean(sub_county_df["HourlyRelativeHumidity"])
        avg_wb_temp = mean(sub_county_df["HourlyWetBulbTemperature"])
        avg_wind_speed = mean(sub_county_df["HourlyWindSpeed"])

        sub_county_df["DailyPrecipitation"] = (
            pd.to_numeric(sub_county_df["DailyPrecipitation"],
                  errors='coerce')
                    .fillna(0)
            )

        precip = sum(sub_county_df["DailyPrecipitation"])

        
        to_add = [county, curr_date, fire_occ_curr, acres_burned_curr, avg_dp_temp, avg_rel_hum, avg_wb_temp, avg_wind_speed, precip, curr_pop_density, curr_lat, curr_long]
        d[(county, curr_date)] = to_add


df = pd.DataFrame.from_dict(d, orient='index', columns=columns)
df = df[columns]
df.to_csv ('all_data_newest.csv', index=False, columns=columns, header=columns)

