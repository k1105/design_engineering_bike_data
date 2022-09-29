import pandas as pd
import csv

station = pd.read_csv(
    'hello-cycling/data/埼玉県/xy_projected_stations.csv', index_col=0)
weight = pd.read_csv('hello-cycling/data/埼玉県/weight.csv', index_col=0)
name = pd.read_csv('hello-cycling/data/埼玉県/station_name.csv', index_col=0)
begin_id = 673


path = "hello-cycling/merged/埼玉県/close_staition_from_" + \
    name.loc[begin_id]['name']+"_with_xyz_name.csv"
data = pd.read_csv("hello-cycling/data/埼玉県/close_staition_from_" +
                   name.loc[begin_id]['name']+".csv", index_col=0)

header = ["x", "y", "z", "name", "dist"]
with open(path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    writer.writerow([station.at[begin_id, 'x'], station.at[begin_id, 'y'], weight.at[begin_id, 'weight'],  name.at[begin_id,
                                                                                                                   'name'], 0])
    for index, row in data.iterrows():
        writer.writerow([station.at[index, 'x'], station.at[index, 'y'],
                        weight.at[index, 'weight'], name.at[index,
                                                            'name'], row['dist']])
