from module import ProjectedMercator as pm
import csv
import pandas as pd

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

for pref in pref_list:
    print(pref)
    pos = []
    indices = []
    df = pd.read_csv('hello-cycling/data/'+pref+'/station.csv', index_col=0)

    if len(df) != 0:
        for index, station in df.iterrows():
            pos.append([station['lon'], station['lat']])
            indices.append(index)

        xy_pos = pm.ProjectedMercator(pos, 100)

        path = './hello-cycling/data/'+pref+'/xy_projected_stations.csv'
        with open(path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(['id', 'x', 'y'])
            for i in range(len(xy_pos)):
                writer.writerow([indices[i], xy_pos[i][0], xy_pos[i][1]])
