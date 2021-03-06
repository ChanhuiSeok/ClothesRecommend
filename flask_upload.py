import os
import sys
import requests
import json
import cv2
from matplotlib.image import imread
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import time, random

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 300 * 1024

# 이미지 저장 이름

## 포즈 리스트를 저장하는 함수
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


## 이미지 마커 표시 함수
def get_image_marker(image_name, arr):
    # image = cv2.imread(image_name, cv2.IMREAD_COLOR)
    image = imread('./uploads/'+image_name)
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
    plt.savefig('./uploads/' + "after_" + image_name)
    # plt.show()

## 이미지 처리 함수
def get_processed_image(img_name):
    # API 관련 정보
    client_id = "ckxz1tuwnd"
    client_secret = "gQjrBxqc5zoob4chVie5OKmpgS0WyRZe5exik5EF"
    url = "https://naveropenapi.apigw.ntruss.com/vision-pose/v1/estimate"
    image_name = './uploads/' + img_name
    print(image_name)

    # 분석 이미지
    files = {
        'image': open(image_name, 'rb')
    }
    headers = {
        'X-NCP-APIGW-API-KEY-ID': client_id,
        'X-NCP-APIGW-API-KEY': client_secret \
    }
    pose_list = get_pose_list(url, files, headers)
    get_image_marker(img_name, pose_list)



#첫페이지 라우팅(index.html)
@app.route('/')
def index():
        return render_template(
            "index.html"
        )


#업로드 HTML 렌더링
@app.route('/upload')
def render_file():
    return render_template('upload.html')

#파일업로드
@app.route('/fileUpload', methods = ['GET','POST'])
def upload_file():
    value = int(time.time() + random.randint(1, 100)) % 10000
    save_name = str(value)

    if request.method == 'POST':
        f = request.files['file']
        f.save('./uploads/' + save_name + secure_filename(f.filename))
        print('저장 완료')
        get_processed_image(save_name + secure_filename(f.filename))
        return 'uploads 디렉토리 -> 파일 업로드 -> 처리한 이미지 저장 성공!'


if __name__ == '__main__':
    app.run(debug = True)