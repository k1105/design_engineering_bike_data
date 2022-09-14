from email import header
from module import GetEdges as ge
import csv

network = ge.GetEdges(500)
path = './data/network500.csv'
header = ["begin", "end"]
with open(path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    for edge in network:
        writer.writerow([edge[0],
                        edge[1]])
