# export csv file
import os
import csv
import requests

pref_list = ["北海道",
             "青森県",
             "岩手県",
             "宮城県",
             "秋田県",
             "山形県",
             "福島県",
             "茨城県",
             "栃木県",
             "群馬県",
             "埼玉県",
             "千葉県",
             "東京都",
             "神奈川県",
             "新潟県",
             "富山県",
             "石川県",
             "福井県",
             "山梨県",
             "長野県",
             "岐阜県",
             "静岡県",
             "愛知県",
             "三重県",
             "滋賀県",
             "京都府",
             "大阪府",
             "兵庫県",
             "奈良県",
             "和歌山県",
             "鳥取県",
             "島根県",
             "岡山県",
             "広島県",
             "山口県",
             "徳島県",
             "香川県",
             "愛媛県",
             "高知県",
             "福岡県",
             "佐賀県",
             "長崎県",
             "熊本県",
             "大分県",
             "宮崎県",
             "鹿児島県",
             "沖縄県", ]


header = ['id', 'name']
url = "https://api-public.odpt.org/api/v4/gbfs/hellocycling/station_information.json"
# requests.getを使うと、レスポンス内容を取得できるのでとりあえず変数へ保存
response = requests.get(url)
# response.json()でJSONデータに変換して変数へ保存
jsonData = response.json()

path = './hello-cycling/data/station_prefecture.csv'
with open(path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    for station in jsonData['data']['stations']:
        pref = "NONE"
        for cand in pref_list:
            if station['address'].startswith(cand):
                pref = cand
                break
        writer.writerow([station['station_id'],
                        pref])
