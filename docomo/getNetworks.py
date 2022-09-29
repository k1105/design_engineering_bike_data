from module import GetEdges as ge
import csv

for threthold in range(500, 5500, 500):
    network = ge.GetEdges(threthold)
    path = './data/network'+str(threthold)+'.csv'
    header = ["begin", "end"]
    with open(path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        for edge in network:
            writer.writerow([edge[0],
                            edge[1]])
