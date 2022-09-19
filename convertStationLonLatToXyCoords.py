import math
import pandas as pd
import csv
from module import GetAllStationPositions as gap

station = pd.read_csv('data/csv_eki_13.csv', encoding="shift-jis")

path = "merged/xy_projected_train_stations.csv"


# 緯度経度についてメルカトル座標に変換

width = 100
pos = gap.GetAllStationPositions()

lon_sorted_pos = sorted(pos, key=lambda x: x[0])
lat_sorted_pos = sorted(pos, key=lambda x: x[1])

lon_min = lon_sorted_pos[0][0]
lon_max = lon_sorted_pos[-1][0]
lat_min = lat_sorted_pos[0][1]
lat_max = lat_sorted_pos[-1][1]

l = (lon_min + lon_max) / 2
boxWidth = ((lon_max - lon_min) * math.pi) / 180
scale = 1
if boxWidth != 0:
    scale = width / boxWidth

x = (math.pi * (lon_min - l)) / 180
y = math.log(math.tan(math.pi * (0.25 + lat_max / 360)))

header = ["station_name", "x", "y"]
with open(path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    for index, row in station.iterrows():
        coord = [row['station_lon'], row['station_lat']]
        pos_x = (math.pi * (coord[0] - l)) / 180 - x
        pos_y = y - math.log(math.tan(math.pi*(9.25 + coord[1] / 360)))
        writer.writerow([row['station_name'], pos_x * scale, pos_y * scale])
