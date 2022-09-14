from module import CalcDistance as cd
from module import GetAllStationPositions as gap
from module import GetAllStationIndices as gai


def GetEdges(threthold):
    pos = gap.GetAllStationPositions()
    indices = gai.GetAllStationIndices()
    network = set()
    stationCount = len(pos)  # 自転車のステーションの数

    for target in range(stationCount):
        for i in range(stationCount):
            if i != target:
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
