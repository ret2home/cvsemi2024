import sys
import json
from lib import wave_data, cos_similarity


# 類似度を各都道府県について計算する
def similar_ranking(file_path, wv_pres, show=False):
    wv = wave_data(file_path, show)

    results = []
    for prefecture in wv_pres.keys():
        results.append((cos_similarity(wv, wv_pres[prefecture]), prefecture))
    results = sorted(results)
    return results


if __name__ == "__main__":
    with open("./data.json") as f:
        wv_pres = json.load(f)

    res = similar_ranking(sys.argv[1], wv_pres, True)

    # 上位候補 5 つの都道府県を出力
    print("result:")
    for i in range(5):
        print(res[i][1], 100 - res[i][0] / 90 * 100)
