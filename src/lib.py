import cv2
import math
import matplotlib.pyplot as plt
import numpy as np


# (x1,y1) と (x2,y2) を結ぶ線分と、原点を通る偏角 theta (度数法) の交点を求める
def calculate_intersection(x1, y1, x2, y2, theta):
    x3, y3 = 0, 0
    if theta == 90:
        x4, y4 = 0, 1000
    elif theta == 270:
        x4, y4 = 0, -1000
    else:
        x4, y4 = (
            1000 * math.cos(theta / 180 * math.pi),
            1000 * math.sin(theta / 180 * math.pi),
        )
    # 線分1の係数
    A1 = y2 - y1
    B1 = x1 - x2
    C1 = x2 * y1 - x1 * y2

    # 線分2の係数
    A2 = y4 - y3
    B2 = x3 - x4
    C2 = x4 * y3 - x3 * y4

    # 行列式を計算
    det = A1 * B2 - A2 * B1

    if det == 0:
        # 行列式がゼロの場合、線分は平行または一致している
        return None

    # 交点を計算
    x = (B1 * C2 - B2 * C1) / det
    y = (A2 * C1 - A1 * C2) / det

    eps = 1e-6

    # 交点が両方の線分上にあるか確認
    if (
        min(x1, x2) - eps <= x <= max(x1, x2) + eps
        and min(y1, y2) - eps <= y <= max(y1, y2) + eps
        and min(x3, x4) - eps <= x <= max(x3, x4) + eps
        and min(y3, y4) - eps <= y <= max(y3, y4) + eps
    ):
        return (x, y)
    else:
        return None


# 元画像、輪郭データ、偏角ごとの距離データを表示する
def show_images(img, contour, wv):
    M = cv2.moments(contour)
    # 重心座標
    cx = M["m10"] / M["m00"]
    cy = M["m01"] / M["m00"]
    contour_image = np.ones_like(img) * 255
    cv2.drawContours(contour_image, [contour], -1, (0, 0, 0), 2)  # 輪郭を描画

    # 画像を表示
    plt.subplot(2, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Original Image")

    plt.subplot(2, 2, 2)
    plt.imshow(cv2.cvtColor(contour_image, cv2.COLOR_BGR2RGB))
    plt.scatter([cx], [cy], s=1)  # 重心をプロット
    plt.title("Contours")

    ax = plt.subplot(2, 2, 3)
    xx, yy = [], []
    for i in range(360):
        x = math.cos(i / 180 * math.pi) * wv[i]
        y = math.sin(i / 180 * math.pi) * wv[i]
        xx.append(x)
        yy.append(-y)
    ax.scatter(xx, yy,s=1)
    ax.scatter([0],[0],s=3)
    ax.set_aspect("equal")

    plt.tight_layout()
    plt.show()
    plt.close()


# 輪郭の集合から最も長い輪郭を求める
def longest_contour(contours):
    mx, mx_idx = 0, -1
    for idx, contour in enumerate(contours):
        if mx < len(contour):
            mx = len(contour)
            mx_idx = idx
    return contours[mx_idx]


# 偏角[0,360)度で最も重心から離れた点までの距離を求める
def wave_data(file_path, show=False):
    # 輪郭を抽出する
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    contour = longest_contour(contours)

    M = cv2.moments(contour)
    cx = M["m10"] / M["m00"]
    cy = M["m01"] / M["m00"]

    dist_round = [0] * 360

    for i in range(len(contour)):
        x1 = contour[i][0][0] - cx
        y1 = contour[i][0][1] - cy
        x2 = contour[(i + 1) % len(contour)][0][0] - cx
        y2 = contour[(i + 1) % len(contour)][0][1] - cy

        for theta in range(0, 360):
            res = calculate_intersection(x1, y1, x2, y2, theta)
            if res is not None:
                dis = math.sqrt(res[0] ** 2 + res[1] ** 2)
                dist_round[theta] = max(dist_round[theta], dis)

    mean_dist_round=sum(dist_round)/360
    wv = [d / mean_dist_round for d in dist_round]

    if show:
        show_images(image, contour, wv)

    return wv


# ベクトルの角度を求める
def cos_similarity(A, B):
    norm_A = 0
    norm_B = 0
    for a in A:
        norm_A += a * a
    for b in B:
        norm_B += b * b
    norm_A = math.sqrt(norm_A)
    norm_B = math.sqrt(norm_B)
    dot = 0
    for i in range(len(A)):
        dot += A[i] * B[i]
    
    # eps
    arg=dot/norm_A/norm_B
    if arg>1:
        arg=1

    return math.degrees(math.acos(arg))