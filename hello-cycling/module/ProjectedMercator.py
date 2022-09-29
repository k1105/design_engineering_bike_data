import math

# 緯度経度についてメルカトル座標に変換


def ProjectedMercator(pos, width):
    # pos = [[lon, lat], [lon, lat], [lon, lat], ...]
    res = []

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

    for coord in pos:
        pos_x = (math.pi * (coord[0] - l)) / 180 - x
        pos_y = y - math.log(math.tan(math.pi*(9.25 + coord[1] / 360)))
        res.append([pos_x * scale, pos_y * scale])

    return res
