import os
import math
import json
import requests
from module import CalcDistance as cd
# https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/station_information.json
# 上記のURLからjsonを取得
import csv
import pandas as pd
import random

df = pd.read_csv('hello-cycling/data/station.csv', index_col=0)
df_name = pd.read_csv('hello-cycling/data/station_name.csv', index_col=0)
df_pref = pd.read_csv('hello-cycling/data/station_prefecture.csv', index_col=0)
ex_pref_list = ["東京都", "神奈川県", "埼玉県", "大阪府",
                "静岡県", "千葉県", "兵庫県", "沖縄県", "京都府", "長野県", "岐阜県", "愛知県", "新潟県", "栃木県", "香川県", "佐賀県", "福岡県", "岩手県", "和歌山県", "熊本県", "茨城県", "愛媛県"]

for i in range(10):

    print('\n')
    print(str(i+1)+'th attempt')

    pref = "東京都"

    while pref in ex_pref_list:
        target_id = random.choice(df.index.values)
        target_data = df.loc[target_id]
        pref = df_pref.at[target_id, 'name']

    print(target_id)
    print(pref)
    if pref in ex_pref_list:
        print('next')
        continue

    limited_df = pd.read_csv('hello-cycling/data/'+pref +
                             '/station.csv', index_col=0)
    limited_df_name = pd.read_csv(
        'hello-cycling/data/'+pref+'/station_name.csv', index_col=0)

    target_pos = [target_data['lon'], target_data['lat']]

    stations = []

    for index, current in limited_df.iterrows():
        if index != target_id:
            current_pos = [current['lon'], current['lat']]
            dist = cd.CalcDistance(current_pos, target_pos)
            stations.append(
                [index, dist])

    stations.sort(key=lambda data: data[1])

    header = ['id', 'dist']

    path = 'hello-cycling/data/'+pref+'/close_staition_from_' + \
        limited_df_name.loc[target_id]['name']+'.csv'
    with open(path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        for station in stations:
            writer.writerow(station)

    station = pd.read_csv(
        'hello-cycling/data/'+pref+'/xy_projected_stations.csv', index_col=0)
    weight = pd.read_csv('hello-cycling/data/'+pref+'/weight.csv', index_col=0)
    name = pd.read_csv('hello-cycling/data/'+pref +
                       '/station_name.csv', index_col=0)

    path = "hello-cycling/merged/"+pref+"/close_staition_from_" + \
        name.loc[target_id]['name']+"_with_xyz_name.csv"
    data = pd.read_csv("hello-cycling/data/"+pref+"/close_staition_from_" +
                       name.loc[target_id]['name']+".csv", index_col=0)

    header = ["x", "y", "z", "name", "dist"]
    with open(path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        writer.writerow([station.at[target_id, 'x'], station.at[target_id, 'y'], weight.at[target_id, 'weight'],  name.at[target_id,
                                                                                                                          'name'], 0])
        for index, row in data.iterrows():
            writer.writerow([station.at[index, 'x'], station.at[index, 'y'],
                            weight.at[index, 'weight'], name.at[index,
                                                                'name'], row['dist']])

    x = -0.0024023409956149796
    y = 0.6694034165211005
    scale = 20813.03199307075
    l = 139.708739

    begin_lon = str(df.at[target_id, 'lon'])
    begin_lat = str(df.at[target_id, 'lat'])

    header = ['x', 'y', 'rot', 'dist', 'total_dist']

    path = 'hello-cycling/data/'+pref+'/route_from_' + \
        limited_df_name.loc[target_id]['name'] + '.csv'

    with open(path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)

        for index, row in limited_df.iterrows():
            print("\r"+str(index), end="")

            end_lon = str(row['lon'])
            end_lat = str(row['lat'])

            if [begin_lon, begin_lat] != [end_lon, end_lat]:

                url = "https://api.mapbox.com/directions/v5/mapbox/cycling/"+begin_lon+","+begin_lat+";"+end_lon+","+end_lat + \
                    "?geometries=geojson&access_token=pk.eyJ1Ijoia241bXIiLCJhIjoiY2twNm9lZTBlMDF5dDJxbGlpcndvZmwxdCJ9.G0tpfqYkfanFVqc_HNZ-Mw"
                # requests.getを使うと、レスポンス内容を取得できるのでとりあえず変数へ保存
                response = requests.get(url)

                try:
                    pos = response.json()[
                        'routes'][0]['geometry']['coordinates']

                    conv_pos = []

                    for coord in pos:
                        pos_x = (math.pi * (coord[0] - l)) / 180 - x
                        pos_y = y - \
                            math.log(math.tan(math.pi*(9.25 + coord[1] / 360)))

                        # 変換後のxy座標
                        conv_x = pos_x * scale
                        conv_y = pos_y * scale

                        conv_pos.append([conv_x, conv_y])

                    origin = conv_pos[0][1]
                    conv_pos = list(
                        map(lambda x: [x[0], 2*origin-x[1]], conv_pos))

                    total_dist = 0

                    data = []
                    for i in range(len(conv_pos)-1):
                        c_x = conv_pos[i][0]
                        n_x = conv_pos[i+1][0]
                        c_y = conv_pos[i][1]
                        n_y = conv_pos[i+1][1]

                        dist = math.sqrt((c_x-n_x)**2+(c_y-n_y)**2)
                        total_dist += dist
                        rot = math.atan2((c_y-n_y), (c_x-n_x)) / \
                            math.pi*180 + 180
                        writer.writerow([c_x, c_y, rot, dist, total_dist])
                except IndexError as e:
                    print('no route found')
