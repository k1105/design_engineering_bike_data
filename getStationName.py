# export csv file
import os
import csv
import requests

header = ['id', 'name']
url = "https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/station_information.json"
# requests.getを使うと、レスポンス内容を取得できるのでとりあえず変数へ保存
response = requests.get(url)
# response.json()でJSONデータに変換して変数へ保存
jsonData = response.json()

path = './data/station_name.csv'
with open(path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    for station in jsonData['data']['stations']:
        writer.writerow([station['station_id'],
                        station['name']])
