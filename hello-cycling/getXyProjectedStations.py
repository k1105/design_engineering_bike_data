from module import ProjectedMercator as pm
import csv
import pandas as pd

# #このJSONオブジェクトは、連想配列（Dict）っぽい感じのようなので
# #JSONでの名前を指定することで情報がとってこれる
pos = []
indices = []
df = pd.read_csv('hello-cycling/data/埼玉県/station.csv', index_col=0)

for index, station in df.iterrows():
    pos.append([station['lon'], station['lat']])
    indices.append(index)

xy_pos = pm.ProjectedMercator(pos, 100)

path = './hello-cycling/data/埼玉県/xy_projected_stations.csv'
with open(path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(['id', 'x', 'y'])
    for i in range(len(xy_pos)):
        writer.writerow([indices[i], xy_pos[i][0], xy_pos[i][1]])
