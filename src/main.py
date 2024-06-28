import sys
import json
from lib import wave_data, cos_similarity


# 類似度を各都道府県について計算する
def similar_ranking(file_path, prefectures, wv_pres, show=False):
    wv = wave_data(file_path, show)

    results = []
    for prefecture in prefectures:
        results.append((cos_similarity(wv, wv_pres[prefecture]), prefecture))
    results = sorted(results)
    return results


if __name__ == "__main__":
    prefectures = [
        "okinawa",
        "kagoshima",
        "miyazaki",
        "oita",
        "kumamoto",
        "nagasaki",
        "saga",
        "fukuoka",
        "kochi",
        "ehime",
        "kagawa",
        "tokushima",
        "yamaguchi",
        "hiroshima",
        "okayama",
        "shimane",
        "tottori",
        "wakayama",
        "nara",
        "hyogo",
        "osaka",
        "kyoto",
        "shiga",
        "mie",
        "aichi",
        "shizuoka",
        "gifu",
        "nagano",
        "yamanashi",
        "ishikawa",
        "fukui",
        "toyama",
        "niigata",
        "kanagawa",
        "tokyo",
        "chiba",
        "saitama",
        "gunma",
        "tochigi",
        "ibaraki",
        "fukushima",
        "yamagata",
        "akita",
        "miyagi",
        "iwate",
        "aomori",
        "hokkaido",
    ]
    with open("./data.json") as f:
        wv_pres = json.load(f)

    res = similar_ranking(sys.argv[1], prefectures, wv_pres, True)

    # 上位候補 5 つの都道府県を出力
    print("result:")
    for i in range(5):
        print(res[i][1], 100 - res[i][0] / 90 * 100)
