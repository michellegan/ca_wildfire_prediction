import pandas as pd
import sys
import datetime, calendar
from datetime import date, timedelta


#script to generate dataset linking countydate-> population density
all_data = "./all_data.csv"
all_data = pd.read_csv(all_data, sep=",", header=0)



alameda = "./A-L Counties/Alameda.csv"
butte = "./A-L Counties/Butte.csv"
contra_costa = "./A-L Counties/Contra Costa.csv"
del_norte = "./A-L Counties/Del Norte.csv"
el_dorado = "./A-L Counties/El Dorado.csv"
fresno = "./A-L Counties/Fresno.csv"
humboldt = "./A-L Counties/Humboldt.csv"
inyo = "./A-L Counties/Inyo.csv"
kern = "./A-L Counties/Kern.csv"
kings = "./A-L Counties/Kings.csv"
los_angeles = "./A-L Counties/Los Angeles.csv"

madera = "./M-R/Madera.csv"
marin = "./M-R/Marin.csv"
mariposa = "./M-R/Mariposa.csv"
mendocino = "./M-R/Mendocino.csv"
merced = "./M-R/Merced.csv"
modoc = "./M-R/Modoc.csv"
mono = "./M-R/Mono.csv"
monterey = "./M-R/Monterey.csv"
napa = "./M-R/Napa.csv"
nevada = "./M-R/Nevada.csv"
orange = "./M-R/Orange.csv"
placer = "./M-R/Placer.csv"
riverside = "./M-R/Riverside.csv"

sacramento = "./Sacramento-Siskiyou/Sacramento.csv"
san_benito = "./Sacramento-Siskiyou/San Benito.csv"
san_bernardino = "./Sacramento-Siskiyou/San Bernardino.csv"
san_diego = "./Sacramento-Siskiyou/San Diego.csv"
san_joaquin = "./Sacramento-Siskiyou/San Joaquin.csv"
san_luis_obispo = "./Sacramento-Siskiyou/San Luis Obispo.csv"
san_mateo = "./Sacramento-Siskiyou/San Mateo.csv"
santa_barbara = "./Sacramento-Siskiyou/Santa Barbara.csv"
santa_clara = "./Sacramento-Siskiyou/Santa Clara.csv"
santa_cruz = "./Sacramento-Siskiyou/Santa Cruz.csv"
shasta = "./Sacramento-Siskiyou/Shasta.csv"
siskiyou = "./Sacramento-Siskiyou/Siskiyou.csv"

solano = "./Solano-Yuba/Solano.csv"
sonoma = "./Solano-Yuba/Sonoma.csv"
stanislaus = "./Solano-Yuba/Stanislaus.csv"
tehama = "./Solano-Yuba/Tehama.csv"
trinity = "./Solano-Yuba/Trinity.csv"
tulare = "./Solano-Yuba/Tulare.csv"
tuolumne = "./Solano-Yuba/Tuolumne.csv"
ventura = "./Solano-Yuba/Ventura.csv"
yolo = "./Solano-Yuba/Yolo.csv"
yuba = "./Solano-Yuba/Yuba.csv"

all_data['county'] = all_data['county']
all_data['dates'] = all_data['date']
all_data['fire_occurence'] = all_data['fire_occurrence']
all_data['acres_burned'] = all_data['acres_burned']

all_data = all_data[['county', 'date','fire_occurence', 'acres_burned']] 

#prepare dataframe
columns = ['county', 'date', 'fire_occurrence', 'acres_burned', "avg_dp_temp", "avg_db_temp", "avg_rel_hum", "avg_wb_temp", "avg_wind_speed", "precip"]
d = {}


counties = set(all_data['county'].tolist())

dates = all_data['dates']

counties_col = all_data['county'] = all_data['county']
dates_col = all_data['dates']
fire_occ_col = all_data['fire_occurrence']
acres_burned_col = all_data['acres_burned']

for county in list(counties):
    formatted_county = (county.lower())
    if formatted_county.isspace():
        formatted_county.replace(" ", "_")
    curr_county_file = pd.read_csv(formatted_county, sep=",", header=0)

    date_col = curr_county_file["DATE"]
    avg_dp_temp_col = curr_county_file["DailyAverageDewPointTemperature"]
    avg_db_temp_col = curr_county_file["DailyAverageDryBulbTemperature"]
    avg_rel_hum_col = curr_county_file["DailyAverageRelativeHumidity"]
    avg_wb_temp_col = curr_county_file["DailyAverageWetBulbTemperature"]
    avg_wind_speed_col = curr_county_file["DailyAverageWindSpeed"]
    precip_col = curr_county_file["DailyPrecipitation"]

    j = 0
    for i in range(0, curr_county_file.shape[0], 25):
        curr_date = date_col[i]
        #county_df = counties_col[j]
        #date_df = dates_col[j]
        fire_occ_df = fire_occ_col[j]
        acres_burned_df = acres_burned_col[j]
        avg_dp_temp = avg_dp_temp_col[i] 
        avg_db_temp = avg_db_temp_col[i] 
        avg_rel_hum = avg_rel_hum_col[i]
        avg_wb_temp = avg_wb_temp_col[i]
        avg_wind_speed = avg_wind_speed_col[i]
        precip = precip_col[i] 
        
        to_add = [county, curr_date, fire_occ_df, acres_burned_df, avg_dp_temp, avg_db_temp, avg_rel_hum, avg_wb_temp, avg_wind_speed, precip]
        d[(county, curr_date)] = to_add


df = pd.DataFrame.from_dict(d, orient='index', columns=columns)
df = df[columns]
df.to_csv ('all_data_w_counties.csv', index=False, columns=columns, header=columns)

