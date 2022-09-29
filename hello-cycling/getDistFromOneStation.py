from module import CalcDistance as cd
# https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/station_information.json
# 上記のURLからjsonを取得
import csv
import pandas as pd


target_id = 673
df = pd.read_csv('hello-cycling/data/埼玉県/station.csv', index_col=0)
df_name = pd.read_csv('hello-cycling/data/埼玉県/station_name.csv', index_col=0)
target_data = df.loc[target_id]

target_pos = [target_data['lon'], target_data['lat']]

stations = []

for index, current in df.iterrows():
    if index != target_id:
        current_pos = [current['lon'], current['lat']]
        dist = cd.CalcDistance(current_pos, target_pos)
        stations.append(
            [index, dist])

stations.sort(key=lambda data: data[1])

header = ['id', 'dist']

path = 'hello-cycling/data/埼玉県/close_staition_from_' + \
    df_name.loc[target_id]['name']+'.csv'
with open(path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    for station in stations:
        writer.writerow(station)
