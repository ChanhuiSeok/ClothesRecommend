import os
import sys
import requests
import json
import cv2
from matplotlib.image import imread
import matplotlib.pyplot as plt
import time, random

# 이미지 저장 이름
value = int(time.time() + random.randint(1, 100)) % 10000
save_name = "capture" + str(value)


def get_pose_list(url, files, headers):  # 사람의 포즈(주요 신체부위 18개의 좌표)와 신뢰확률 점수 결과 반환
    # 사람의 포즈(주요 신체부위 18개의 좌표(와 신뢰확률 점수 결과 반환
    # 코(0), 목(1), 오른쪽 어깨(2), 오른쪽 팔꿈치(3), 오른쪽 손목(4), 왼쪽 어깨(5), 왼쪽 팔꿈치(6)
    # 왼쪽 손목(7), 오른쪽 엉덩이(8), 오른쪽 무릎(9), 오른쪽 발목(10), 왼쪽 엉덩이(11)
    # 왼쪽 무릎(12), 왼쪽 발목(13), 오른쪽 눈(14), 왼쪽 눈(15), 오른쪽 귀(16), 왼쪽 귀(17)
    response = requests.post(url, files=files, headers=headers)
    rescode = response.status_code
    pose_list = list()
    if rescode == 200:  # 분석 성공
        pose_list = [json.loads(response.text)]  # json -> list
    else:
        print("Error Code:" + str(rescode))
    return pose_list


# 이미지 마커 표시
def get_image_marker(image_name, arr):
    # image = cv2.imread(image_name, cv2.IMREAD_COLOR)
    image = imread(image_name)
    height, weight = image.shape[:2]
    print(arr)
    arr = arr[0]['predictions'][0]  # list -> dictionary
    print(arr)
    x = []
    y = []
    for key in arr.keys():
        print(arr[key])
        x.append(int(arr[key]['x'] * weight))
        y.append(int(arr[key]['y'] * height))
    implot = plt.imshow(image)
    plt.scatter([10], [20])
    plt.scatter(x, y, c='r', s=40)
    plt.savefig('./uploads/' + save_name)
    # plt.show()


if __name__ == "__main__":
    # API 관련 정보
    client_id = "ckxz1tuwnd"
    client_secret = "gQjrBxqc5zoob4chVie5OKmpgS0WyRZe5exik5EF"
    url = "https://naveropenapi.apigw.ntruss.com/vision-pose/v1/estimate"
    image_name = "capture.PNG"

    # 분석 이미지
    files = {
        'image': open(image_name, 'rb')
    }
    headers = {
        'X-NCP-APIGW-API-KEY-ID': client_id,
        'X-NCP-APIGW-API-KEY': client_secret \
        }

    pose_list = get_pose_list(url, files, headers)

    get_image_marker(image_name, pose_list)
