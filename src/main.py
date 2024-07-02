import sys
import json
from lib import wave_data, cos_similarity

# 類似度を各都道府県について計算する
def similar_ranking(file_path, wv_pres, show=False):
    wv = wave_data(file_path, show)

    wv_diff=[wv[i] for i in range(360)]

    results = []
    for prefecture in wv_pres.keys():
        wv_diff_pre=[wv_pres[prefecture][i] for i in range(360)]
        results.append((cos_similarity(wv_diff, wv_diff_pre), prefecture))
    results = sorted(results)
    return results

def irasutoya(wv_pres):
    cnt=0
    for prefecture in wv_pres.keys():
        res=similar_ranking(f"./cvsemi_irasutoya/{prefecture}.png",wv_pres)
        print("------")
        print(prefecture)
        for i in range(5):
            print(res[i][1],100 - res[i][0] / 90 * 100)
        if prefecture==res[0][1]:
            cnt+=1
    print(cnt)

if __name__ == "__main__":
    with open("./data.json") as f:
        wv_pres = json.load(f)

    #irasutoya(wv_pres)
    #exit(0)

    res = similar_ranking(sys.argv[1], wv_pres, True)

    # 上位候補 5 つの都道府県を出力
    print("result:")
    for i in range(5):
        print(res[i][1], 100 - res[i][0] / 90 * 100)
