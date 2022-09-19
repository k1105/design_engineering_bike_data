import requests
import json
from module import GetAllStationPositions as gap
from module import GetAllStationIndices as gai
import csv


pos = gap.GetAllStationPositions()
indices = gai.GetAllStationIndices()

header = ['id', 'region']

path = 'data/region.csv'
with open(path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)

    for i in range(len(pos)):
        coord = pos[i]
        id = indices[i]
        lon = str(coord[0])
        lat = str(coord[1])

        url = "https://api.mapbox.com/geocoding/v5/mapbox.places/"+lon+","+lat + \
            ".json?&access_token=pk.eyJ1Ijoia241bXIiLCJhIjoiY2twNm9lZTBlMDF5dDJxbGlpcndvZmwxdCJ9.G0tpfqYkfanFVqc_HNZ-Mw"

        # requests.getを使うと、レスポンス内容を取得できるのでとりあえず変数へ保存
        response = requests.get(url)
        # response.json()でJSONデータに変換して変数へ保存
        jsonData = response.json()

        print(jsonData['features'][0]['context'][1]['text'])
        writer.writerow([id, jsonData['features'][0]['context'][1]['text']])
