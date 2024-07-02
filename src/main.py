import sys
import json
from lib import wave_data, cos_similarity
from PIL import Image, ImageDraw, ImageFont
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()


# 類似度を各都道府県について計算する
def similar_ranking(file_path, wv_pres, show=False):
    wv = wave_data(file_path, show)

    wv_diff = [wv[i] for i in range(360)]

    results = []
    for prefecture in wv_pres.keys():
        wv_diff_pre = [wv_pres[prefecture][i] for i in range(360)]
        results.append((cos_similarity(wv_diff, wv_diff_pre), prefecture))
    results = sorted(results)
    return results


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

    background_size = (320, 200)
    background_color = (255, 255, 255)
    background = Image.new("RGBA", background_size, background_color)

    input_image = Image.open(input_image_path).convert("RGBA")
    input_image_position = (
        (background_size[0] - input_image.width) // 2,
        (background_size[1] - input_image.height) // 2,
    )
    background.paste(input_image, input_image_position, input_image)

    draw = ImageDraw.Draw(background)
    font_path = os.getenv("FONT_PATH")
    font_size_1 = 28
    font_size_2 = 24
    font_1 = ImageFont.truetype(font_path, font_size_1)
    font_2 = ImageFont.truetype(font_path, font_size_2)
    text_position_1 = (45 + 10 * (len(output_pref) == 2), 60)
    text_position_2 = (50, 130)
    text_color = (0, 0, 0, 255)
    draw.text(text_position_1, output_pref, font=font_1, fill=text_color)
    draw.text(text_position_2, f"{output_score}点", font=font_2, fill=text_color)
    background.show()
    background.save(output_image_path)