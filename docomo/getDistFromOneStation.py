from module import CalcDistance as cd
# https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/station_information.json
# 上記のURLからjsonを取得
import requests
import json
import csv

url = "https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/station_information.json"

# requests.getを使うと、レスポンス内容を取得できるのでとりあえず変数へ保存
response = requests.get(url)

# response.json()でJSONデータに変換して変数へ保存
jsonData = response.json()


target_id = '00010024'
target_data = list(
    filter(lambda x: x['station_id'] == target_id, jsonData['data']['stations']))[0]

target_pos = [target_data['lon'], target_data['lat']]

stations = []

for i in range(len(jsonData['data']['stations'])):
    current_data = jsonData['data']['stations'][i]
    if current_data['station_id'] != target_id:
        current_pos = [current_data['lon'], current_data['lat']]
        dist = cd.CalcDistance(current_pos, target_pos)
        stations.append(
            [current_data['station_id'], dist])

stations.sort(key=lambda data: data[1])

header = ['id', 'dist']

path = 'data/close_staition_from_' + target_data['name']+'.csv'
with open(path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    for station in stations:
        writer.writerow(station)
