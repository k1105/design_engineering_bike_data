from module import ProjectedMercator as pm

# https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/station_information.json
# 上記のURLからjsonを取得
from textwrap import indent
import requests
import json
import csv

url = "https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/station_information.json"

# requests.getを使うと、レスポンス内容を取得できるのでとりあえず変数へ保存
response = requests.get(url)

# response.json()でJSONデータに変換して変数へ保存
jsonData = response.json()

# #このJSONオブジェクトは、連想配列（Dict）っぽい感じのようなので
# #JSONでの名前を指定することで情報がとってこれる
pos = []
indices = []

for station in jsonData['data']['stations']:
    pos.append([station['lon'], station['lat']])
    indices.append(station['station_id'])

xy_pos = pm.ProjectedMercator(pos, 100)

path = './data/xy_projected_stations.csv'
with open(path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(['id', 'x', 'y'])
    for i in range(len(xy_pos)):
        writer.writerow([indices[i], xy_pos[i][0], xy_pos[i][1]])
