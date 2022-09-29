# https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/station_information.json
# 上記のURLからjsonを取得
import requests
import json


def GetAllStationIndices():
    url = "https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/station_information.json"

    # requests.getを使うと、レスポンス内容を取得できるのでとりあえず変数へ保存
    response = requests.get(url)

    # response.json()でJSONデータに変換して変数へ保存
    jsonData = response.json()

    # #このJSONオブジェクトは、連想配列（Dict）っぽい感じのようなので
    # #JSONでの名前を指定することで情報がとってこれる
    indices = []

    for station in jsonData['data']['stations']:
        indices.append(station['station_id'])

    return indices
