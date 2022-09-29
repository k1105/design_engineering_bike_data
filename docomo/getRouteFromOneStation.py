import requests
import json
import math
import os
import csv
import pandas as pd

x = -0.0024023409956149796
y = 0.6694034165211005
scale = 20813.03199307075
l = 139.708739

station = pd.read_csv('data/station.csv')

begin_lon = "139.763329"
begin_lat = "35.675843"

header = ['x', 'y', 'rot', 'dist', 'total_dist']

path = 'data/route_from_A4-03.東京国際フォーラム（メトロD5出口）.csv'
with open(path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)

    for index, row in station.iterrows():
        print(index)

        end_lon = str(row['lon'])
        end_lat = str(row['lat'])

        # 国際フォーラム 139.763329, 35.675843

        if [begin_lon, begin_lat] != [end_lon, end_lat]:

            url = "https://api.mapbox.com/directions/v5/mapbox/cycling/"+begin_lon+","+begin_lat+";"+end_lon+","+end_lat + \
                "?geometries=geojson&access_token=pk.eyJ1Ijoia241bXIiLCJhIjoiY2twNm9lZTBlMDF5dDJxbGlpcndvZmwxdCJ9.G0tpfqYkfanFVqc_HNZ-Mw"
            # requests.getを使うと、レスポンス内容を取得できるのでとりあえず変数へ保存
            response = requests.get(url)
            pos = response.json()['routes'][0]['geometry']['coordinates']

            conv_pos = []

            for coord in pos:
                pos_x = (math.pi * (coord[0] - l)) / 180 - x
                pos_y = y - math.log(math.tan(math.pi*(9.25 + coord[1] / 360)))

                # 変換後のxy座標
                conv_x = pos_x * scale
                conv_y = pos_y * scale

                conv_pos.append([conv_x, conv_y])

            origin = conv_pos[0][1]
            conv_pos = list(map(lambda x: [x[0], 2*origin-x[1]], conv_pos))

            total_dist = 0

            data = []
            for i in range(len(conv_pos)-1):
                c_x = conv_pos[i][0]
                n_x = conv_pos[i+1][0]
                c_y = conv_pos[i][1]
                n_y = conv_pos[i+1][1]

                dist = math.sqrt((c_x-n_x)**2+(c_y-n_y)**2)
                total_dist += dist
                rot = math.atan2((c_y-n_y), (c_x-n_x))/math.pi*180 + 180
                writer.writerow([c_x, c_y, rot, dist, total_dist])
