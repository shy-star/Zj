import json
import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import csv
'''
在图片中绘制多边形区域
'''
def process_points(img_path, points, output_path):

        # 获取坐标信息,
        points = np.array([points], dtype=np.int32)
        for file in os.listdir(img_path):
            if file.split('.')[-1] in image_format:
                # 读取符合要求的图片并获取图片名称
                im_path = os.path.join(img_path, file)
                img = cv2.imread(im_path)
                img_name = im_path.split('\\')[-1]

                ###绘制mask
                zeros = np.zeros((img.shape), dtype=np.uint8)

                # # 原本thickness = -1表示内部填充,这里不知道为什么会报错,只好不填充了 改用函数cv2.polylines
                #cv2.polylines(img, points, isClosed=True, thickness=5, color=(144, 238, 144))
                mask = cv2.fillPoly(zeros, points, color=color_light_white)  ####填充颜色

                mask_img = cv2.bitwise_and(img, mask)
                ##imshow只能显示uint8格式的图片，但是将mask_img更改为mask_img.astype(np.uint8)后会出现图片失真
                # cv2.imshow("handsome",mask_img.astype(np.uint8))
                # cv2.waitKey(0)
                cv2.imwrite(os.path.join(output_path, '{}.jpg').format(img_name), mask_img)

if __name__ == '__main__':

    #用labeling标记旷场边缘，将旷场边缘关键点存入csv文件中
    with open(r'C:\Users\A1\Desktop\test\labeled-data\CollectedData_zhangji.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i, rows in enumerate(reader):
            if i == 4:
                row = rows
                # row = row[1:]
    # print(row)

    #读取csv的坐标并存入list
    points = []
    for i in range(1,len(row),2):
        x = row[i]
        if x == '':
            break
        else:
            xy = [float(row[i]), float(row[i + 1])]
            points.append(xy)

    image_format = ['png', 'jpg']
    color_light_white = (255, 255, 255)  ##浅黄色


    process_points(
                img_path=r'C:\Users\A1\Desktop\test\labeled-data',
                points=points,
                output_path='./with_mask/'
    )
