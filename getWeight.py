# 都内の全ステーション同士の関係性に基づいて重みづけを行う
# 他のステーションとの距離総和の逆比

# export csv file
import os
import csv
import math
import requests
from module import CalcDistance as cd

url = "https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/station_information.json"
response = requests.get(url)
# response.json()でJSONデータに変換して変数へ保存
jsonData = response.json()


stationCount = len(jsonData['data']['stations'])

header = ['id', 'weight']
path = './data/weight.csv'
with open(path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)

    for target in range(stationCount):
        target_data = jsonData['data']['stations'][target]
        target_pos = [target_data['lon'], target_data['lat']]

        totalScore = 0

        for i in range(stationCount):
            if i != target:
                current_data = jsonData['data']['stations'][i]
                current_pos = [current_data['lon'], current_data['lat']]
                dist = cd.CalcDistance(current_pos, target_pos)
                if dist > 5000:
                    score = 0
                else:
                    score = 10 - math.floor(dist / 500)

                totalScore += score

        writer.writerow([target_data['station_id'], totalScore/100])
