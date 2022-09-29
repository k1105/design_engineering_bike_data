# 緯度経度から２地点間の距離を計算する
import math


def CalcDistance(pos_a, pos_b):
    pi = math.pi
    lng_p = (pos_a[0] / 180) * pi
    lat_p = (pos_a[1] / 180) * pi
    lng_c = (pos_b[0] / 180) * pi
    lat_c = (pos_b[1] / 180) * pi

    dx = lng_c - lng_p
    dy = lat_c - lat_p
    p = (lat_c + lat_p) / 2
    Rx = 6378137  # WGS84に基づく長半径
    E = 0.08181919  # 離心率
    W = math.sqrt(1 - E ** 2 * math.sin(p) ** 2)
    N = Rx / W
    M = (Rx * (1 - E ** 2)) / W ** 3

    return math.sqrt((dy * M) ** 2 + (dx * N * math.cos(p)) ** 2)
