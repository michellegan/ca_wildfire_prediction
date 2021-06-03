import pandas as pd

ALL_DATA = 'all_data_final.csv'
columns = ['county', 'date', 'fire_occurrence', 'acres_burned', "avg_dp_temp", "avg_rel_hum", "avg_wb_temp", "avg_wind_speed", "precip", "pop_density", "latitude", "longitude", "key"]

all_data = pd.read_csv(ALL_DATA, sep=",",header=0)
def get_key(row):
    return row['county'] + row['date']
all_data['key'] = all_data.apply(lambda row: get_key(row), axis=1)

all_data.to_csv ('all_data_final_key.csv', index=False, columns=columns, header=columns)
