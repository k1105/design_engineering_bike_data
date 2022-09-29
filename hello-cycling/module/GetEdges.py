from module import CalcDistance as cd
from module import GetAllStationPositions as gap
from module import GetAllStationIndices as gai
import pandas as pd


def GetEdges(threthold):
    mutual_region = ["千代田区", "中央区", "港区", "新宿区", "文京区", "墨田区",
                     "江東区", "品川区", "目黒区", "大田区", "渋谷区", "中野区", "杉並区", "練馬区"]
    pos = gap.GetAllStationPositions()
    indices = gai.GetAllStationIndices()
    network = set()
    df = pd.read_csv(
        'data/region.csv', index_col=0)
    stationCount = len(pos)  # 自転車のステーションの数

    for target in range(stationCount):
        target_region = df.iloc[target]['region']
        for i in range(stationCount):
            if i != target:
                current_region = df.iloc[i]['region']
                if current_region == target_region or (current_region in mutual_region and target_region in mutual_region):
                    dist = cd.CalcDistance(pos[target], pos[i])
                    if dist <= threthold and threthold-500 < dist:
                        edge = [indices[i], indices[target]]
                        edge.sort()
                        network.add(tuple(edge))

    # set(tuple, tuple, ...) -> list[list, list, ...]
    network = list(map(list, network))

    # edgeFrom = []

    # for i in range(stationCount):
    #   edgeFrom.append([]) ##漸次的に増えるのでi番目の空の配列をここで用意している事になる
    #   indicesFromTargetPoint = [edge for edge in network if edge[0] == i]
    #   edgesFromTargetPoint = list(map(lambda index: [pos[index[0]], pos[index[1]]], indicesFromTargetPoint))
    #   edgeFrom[i] = edgesFromTargetPoint

    # print(edgeFrom[0])
    # ここまでで、あるnodeを起点にしてどんなedgeが存在しているのかが取得できた。以降、トータルを取得。

    return network
