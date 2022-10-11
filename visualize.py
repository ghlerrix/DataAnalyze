import argparse
import json
import os
from xml.etree import ElementTree as ET
import cv2
import numpy as np


class DataVisualization:
    def __init__(self, type, imagePath, labels, outPath, thickness):

        if not os.path.exists(outPath):
            os.makedirs(outPath)

        print('Processing, please wait...')

        if type == 'coco':
            self.cocoVisualize(imagePath, labels, outPath, thickness=thickness)
            
        elif type == 'voc':
             self.vocVisualize(imagePath, labels, outPath, thickness=thickness)

    def cocoVisualize(self, imgPath, jsonPath, out, color=(0, 255, 255), thickness=1):
        # sourcery skip: avoid-builtin-shadow
        with open(jsonPath, 'r') as f:
            annotation_json = json.load(f)

        for img in annotation_json['images']:
            try:
                image_name = img['file_name']  # 读取图片名
                id = img['id']  # 读取图片id
                image_path = os.path.join(imgPath, str(image_name).zfill(5))  # 拼接图像路径
                image = cv2.imdecode(np.fromfile(image_path,dtype=np.uint8),-1)
                # image = cv2.imread(image_path, 1)  # 保持原始格式的方式读取图像
                num_bbox = 0  # 统计一幅图片中bbox的数量

                for i in range(len(annotation_json['annotations'][::])):
                    if annotation_json['annotations'][i - 1]['image_id'] == id:
                        num_bbox = num_bbox + 1
                        x, y, w, h = annotation_json['annotations'][i - 1]['bbox']  # 读取边框
                        image = cv2.rectangle(image, (int(x), int(y)), (int(x + w), int(y + h)), color=color,
                                            thickness=thickness)
                cv2.imwrite(os.path.join(out, image_name), image)
            except Exception as e:
                print(e) 
    
    def vocVisualize(self, imgPath, xmlPath, out, color=(0, 255, 255), thickness=1):
        imgList = os.listdir(imgPath)
        for imgName in imgList:
            name, _ = os.path.splitext(imgName)
            img = os.path.join(imgPath, imgName)
            xml = os.path.join(xmlPath, f'{name}.xml')

            per=ET.parse(xml)
            image = image = cv2.imdecode(np.fromfile(img, dtype=np.uint8),-1)
            imgName = img.split(os.sep)[-1]
            root = per.getroot()

            p=root.findall('object')

            for oneper in p:
                # print(oneper.find('name').text)
                bndbox = oneper.find('bndbox')
                x1 = (int)(bndbox.find('xmin').text)
                y1 = (int)(bndbox.find('ymin').text)
                x2 = (int)(bndbox.find('xmax').text)
                y2 = (int)(bndbox.find('ymax').text)
                # 各参数依次是：图片，添加的文字，左上角坐标(整数)，字体，字体大小，颜色，字体粗细
                # cv2.putText(img, oneper.find('name').text, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                image = cv2.rectangle(image, (x1, y1), (x2, y2), color=color, thickness=thickness)
            cv2.imwrite(os.path.join(out, imgName), image)
    
    def dealChinesePath(self, *paths):
        for p in paths:
            p = p.encode('gbk')
        return paths


def parse_args():
    parser = argparse.ArgumentParser(description='dataset visualize')
    parser.add_argument('type', type=str, help="Dataset format, optional 'voc' and 'coco'")
    parser.add_argument('imgPath', type=str, help="Images path")
    parser.add_argument('labels', type=str, help='Labels path, if it is a voc dataset, it corresponds '
                                               'to the xml directory, if it is a coco dataset, it is the json file '
                                               'path')             
    parser.add_argument('--out', type=str, default='visualizeOut', help='Result output directory')
    parser.add_argument('--thickness', type=int, default=1 ,help="label color thickness")     
    return parser.parse_args()

def main():
    args = parse_args()
    DataVisualization(args.type, args.imgPath, args.labels, args.out, args.thickness)

if __name__ == '__main__':
    main()


