import time
import requests
def crawl(prefecture: str):
    url=f"https://tsukatte.com/wp-content/uploads/2022/11/{prefecture}-prefecture_map_outline_white.png"
    if prefecture=="fukui":
        url="https://tsukatte.com/wp-content/uploads/2022/11/fukui-prefecture_map_white.png"
    data=requests.get(url).content
    with open(f"./prefectures/{prefecture}.png",mode="wb")as f:
        f.write(data)

if __name__ == "__main__":
    prefectures=[
        "okinawa",
        "kagoshima","miyazaki","oita","kumamoto","nagasaki","saga","fukuoka",
        "kochi","ehime","kagawa","tokushima",
        "yamaguchi","hiroshima","okayama","shimane","tottori",
        "wakayama","nara","hyogo","osaka","kyoto","shiga","mie",
        "aichi","shizuoka","gifu","nagano","yamanashi","ishikawa","fukui","toyama","niigata",
        "kanagawa","tokyo","chiba","saitama","gunma","tochigi","ibaraki",
        "fukushima","yamagata","akita","miyagi","iwate","aomori",
        "hokkaido"
    ]
    for prefecture in prefectures:
        crawl(prefecture)
        time.sleep(1)