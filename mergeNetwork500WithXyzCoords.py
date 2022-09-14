import pandas as pd
import csv

path = "merged/network500_with_xyz_coords.csv"
station = pd.read_csv('data/xy_projected_stations.csv', index_col=0)
weight = pd.read_csv('data/weight.csv', index_col=0)
network = pd.read_csv('data/network500.csv')

header = ["begin_x", "begin_y", "begin_z", "end_x", "end_y", "end_z"]
with open(path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    for index, row in network.iterrows():
        writer.writerow([station.at[row['begin'], 'x'], station.at[row['begin'], 'y'],
                         weight.at[row['begin'], 'weight'], station.at[row['end'],
                                                                       'x'], station.at[row['end'], 'y'],
                         weight.at[row['end'], 'weight']])
