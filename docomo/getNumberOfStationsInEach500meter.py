# https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/station_information.json
# 上記のURLからjsonを取得
import requests
import json
import csv
import math
from module import CalcDistance as cs

url = "https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/station_information.json"

# requests.getを使うと、レスポンス内容を取得できるのでとりあえず変数へ保存
response = requests.get(url)

# response.json()でJSONデータに変換して変数へ保存
jsonData = response.json()

# #このJSONオブジェクトは、連想配列（Dict）っぽい感じのようなので
# #JSONでの名前を指定することで情報がとってこれる
pos = []
for station in jsonData['data']['stations']:
    pos.append([station['lon'], station['lat']])

# outのcsv: "id", "500", "1000", "1500", "2000", "2500", "3000", "3500", "4000", "4500", "5000"
header = ["id", "M500", "M1000", "M1500", "M2000",
          "M2500", "M3000", "M3500", "M4000", "M4500", "M5000"]

path = 'data/number_of_stations_in_each_500meter.csv'
with open(path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)

    for target_data in jsonData['data']['stations']:
        # 全ての点に於いて、２点間の距離を計算
        # ある点をtargetとして選択
        # 配列count[10]を用意。
        count = [0] * 10
        target_id = target_data['station_id']
        target_pos = [target_data['lon'], target_data['lat']]

        for current_data in jsonData['data']['stations']:
            if current_data != target_data:
                current_pos = [current_data['lon'], current_data['lat']]
                dist = cs.CalcDistance(current_pos, target_pos)
                # dist計算-> val = floor(dist / 500)について、val < 10 (=5000m)の場合、count[val]をincrement.
                if math.floor(dist/500) < 10:
                    count[math.floor(dist/500)] += 1

        # targetとして選択された点とそれ以外の点との距離を求め、sort. 500m間隔、5000mまでに接続されるstationの数をそれぞれ記録

        # targetのid, *countでwriterow.
        writer.writerow(["ST"+target_id, *list(map(str, count))])
