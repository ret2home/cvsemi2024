import sys
import json
from lib import similar_ranking,dragon
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()


def irasutoya(wv_pres):
    cnt = 0
    for prefecture in wv_pres.keys():
        res = similar_ranking(f"./cvsemi_irasutoya/{prefecture}.png", wv_pres)
        print("------")
        print(prefecture)
        for i in range(5):
            print(res[i][1], 100 - res[i][0] / 90 * 100)
        if prefecture == res[0][1]:
            cnt += 1
    print(cnt)


if __name__ == "__main__":
    with open("./data.json") as f:
        wv_pres = json.load(f)
    with open("./prefectures.json") as f:
        prefectures = json.load(f)

    # irasutoya(wv_pres)
    # exit(0)

    res = similar_ranking(sys.argv[1], wv_pres, True)
    output_pref = prefectures[res[0][1]]
    output_score = int(100 - res[0][0] / 90 * 100)

    input_image_path = "./dragon.png"
    output_image_path = "./output.png"
    font_path = "./NotoSansJP-Medium.ttf"

    dragon(input_image_path,output_image_path,font_path,output_pref,output_score,True)