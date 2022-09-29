# get correlation coefficient of each station
import pandas as pd
import math
import csv

target_id = "00010024"

res = []

threthold = 0.4
df = pd.read_csv('data/number_of_stations_in_each_500meter.csv', index_col=0)

data1 = df.loc["ST"+target_id]
ave1 = 0

for val in data1:
    ave1 += val
ave1 /= 10

# 分散 var1, var2: Σ(値-平均)^2
var1 = 0

for val in data1:
    var1 += (val-ave1)**2

for index, data2 in df.iterrows():

    # 指定されたstation_idとその他全てのstation_idとの相関係数を求める
    # number_of_~~のファイルからカラムをidで検索、取得された2つのカラムについて、
    # [1]~[10]番目の要素を引っ張り出し、それぞれについて、平均、分散、共分散を計算
    # 平均 ave1, ave2：[1]~[10]の値を足して10で割る
    ave2 = 0

    for val in data2:
        ave2 += val
    ave2 /= 10

    # 分散 var1, var2: Σ(値-平均)^2
    var2 = 0

    for val in data2:
        var2 += (val-ave2)**2

    # 共分散 cov: Σ(値-平均)(値-平均)

    cov = 0

    for i in range(10):
        cov += (data1[i]-ave1)*(data2[i]-ave2)

    # 閾値以上の相関係数の値を持つデータについてはそのidと相関係数の値を出力
    cor = cov/(math.sqrt(var1)*math.sqrt(var2))

    # print(cor)

    if cor < threthold:
        res.append([data2.name, cor])

print(res)
