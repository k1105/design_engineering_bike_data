import pandas as pd
import csv

station = pd.read_csv('data/xy_projected_stations.csv', index_col=0)
weight = pd.read_csv('data/weight.csv', index_col=0)
name = pd.read_csv('data/station_name.csv', index_col=0)
begin_id = "00010024"


path = "data/close_staition_from_A4-03.東京国際フォーラム（メトロD5出口）_with_xyz_name.csv"
data = pd.read_csv('data/close_staition_from_A4-03.東京国際フォーラム（メトロD5出口）.csv')

header = ["x", "y", "z", "name", "dist"]
with open(path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    for index, row in data.iterrows():
        writer.writerow([station.at[row['id'], 'x'], station.at[row['id'], 'y'],
                        weight.at[row['id'], 'weight'], name.at[row['id'],
                                                                'name'], row['dist']])
