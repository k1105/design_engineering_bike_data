import pandas as pd
import csv
import math
import os
from module import CalcDistance as cd

pref = "京都府"

if os.path.isdir('hello-cycling/data/' + pref) == False:
    os.makedirs('hello-cycling/data/' + pref)

st_path = "hello-cycling/data/"+pref+"/station.csv"
st_name_path = "hello-cycling/data/"+pref+"/station_name.csv"
weight_path = "hello-cycling/data/"+pref+"/weight.csv"
st_pos = pd.read_csv('hello-cycling/data/station.csv', index_col=0)
st_names = pd.read_csv('hello-cycling/data/station_name.csv', index_col=0)
st_prefs = pd.read_csv(
    'hello-cycling/data/station_prefecture.csv', index_col=0)

index_list = []

for index, p in st_prefs.iterrows():
    if p['name'] == pref:
        index_list.append(index)

with open(st_name_path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(['id', 'name'])
    for id in index_list:
        writer.writerow([id, st_names.loc[id]['name']])

with open(st_path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(['id', 'lon', 'lat'])
    for id in index_list:
        writer.writerow([id, st_pos.loc[id]['lon'], st_pos.loc[id]['lat']])

with open(weight_path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(['id', 'weight'])

    for target in index_list:
        target_pos = [st_pos.loc[target]['lon'], st_pos.loc[target]['lat']]

        totalScore = 0

        for current in index_list:
            if current != target:
                current_pos = [st_pos.loc[current]
                               ['lon'], st_pos.loc[current]['lat']]
                dist = cd.CalcDistance(current_pos, target_pos)
                if dist > 5000:
                    score = 0
                else:
                    score = 10 - math.floor(dist / 500)

                totalScore += score

        writer.writerow([target, totalScore/100])
