import cv2
import sys
import numpy as np

def calculate_similarity(prefecture,contours):
    im_pre=cv2.imread(f"./prefectures/{prefecture}.png")
    gray_pre=cv2.cvtColor(im_pre,cv2.COLOR_BGR2GRAY)
    ret_pre,binary_pre=cv2.threshold(gray_pre,150,255,cv2.THRESH_BINARY)

    contours_pre, hierarchy_pre = cv2.findContours(binary_pre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mx_len,pre_mx_len=0,0
    mx_idx,pre_mx_idx=-1,-1
    for i in range(len(contours)):
        if mx_len<len(contours[i]):
            mx_len=len(contours[i])
            mx_idx=i
    for i in range(len(contours_pre)):
        if pre_mx_len<len(contours_pre[i]):
            pre_mx_len=len(contours_pre[i])
            pre_mx_idx=i

    return cv2.matchShapes(contours[mx_idx], contours_pre[pre_mx_idx], cv2.CONTOURS_MATCH_I1, 0)

if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("Invalid argument.")
        exit(1)
    
    im=cv2.imread(sys.argv[1])
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    ret,binary=cv2.threshold(gray,150,255,cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #img_blank = np.ones_like(im) * 255
    #img_contour_only = cv2.drawContours(img_blank, contours, -1, (0,0,0), 3)
    #cv2.imshow("window",cv2.cvtColor(img_contour_only, cv2.COLOR_BGR2RGB))
    #cv2.waitKey(0)

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

    results=[]
    for prefecture in prefectures:
        results.append((calculate_similarity(prefecture,contours),prefecture))
    results=sorted(results)
    for i in range(5):
        print(results[i][1],results[i][0])