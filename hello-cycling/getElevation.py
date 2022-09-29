from email import header
import requests
import json
import math
import csv
import pandas as pd
import math

station = pd.read_csv('hello-cycling/data/station.csv', index_col=0)
path = 'hello-cycling/data/station_elevation.csv'
header = ['id', 'min', 'max', 'mean']

with open(path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)

    i = 0

    for index, row in station.iterrows():
        i += 1
        print('/r'+str(i), end='')
        url = "https://api.mapbox.com/v4/mapbox.mapbox-terrain-v2/tilequery/" + \
            str(row['lon'])+","+str(row['lat']) + \
            ".json?layers=contour&limit=50&access_token=pk.eyJ1Ijoia241bXIiLCJhIjoiY2twNm9lZTBlMDF5dDJxbGlpcndvZmwxdCJ9.G0tpfqYkfanFVqc_HNZ-Mw"
        # requests.getを使うと、レスポンス内容を取得できるのでとりあえず変数へ保存
        response = requests.get(url)
        jsonData = response.json()
        try:
            elevations = list(
                map(lambda feature: feature['properties']['ele'], jsonData['features']))
            writer.writerow([index, min(elevations), max(
                elevations), sum(elevations)/len(elevations)])
        except KeyError as e:
            print('no features')
            writer.writerow([index, 0, 0, 0])
