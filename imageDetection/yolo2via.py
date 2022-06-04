from via3_tool import Via3Json
import pickle
import csv
from collections import defaultdict
import os
import cv2
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--yoloLabel_dir', default='./chooseVideoFrameYolov5/exp/labels',type=str, help="Label path for yolov5")
parser.add_argument('--image_dir', default='./chooseVideoFrame',type=str, help="Path of video frames")

arg = parser.parse_args()

#坐标格式转化 xywh代表：中心点与宽长，xyxy代表左上角点与右下角点
def xywh2xyxy(box):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    temp = box.copy()
    temp[0] = float(box[0]) - float(box[2]) / 2  # top left x
    temp[1] = float(box[1]) - float(box[3]) / 2  # top left y
    temp[2] = float(box[0]) + float(box[2]) / 2 # bottom right x
    temp[3] = float(box[1]) + float(box[3]) / 2  # bottom right y
    return temp

#最后的via产生的标注文件，viaDetectionPath为存放标注文件的路径
viaDetectionPath = arg.image_dir + '/' + 'detection.json'

via3 = Via3Json(viaDetectionPath, mode='dump')

#计数有多少图片（即标注文件数量）
num_images = 0
for root, dirs, files in os.walk(arg.image_dir, topdown=False):
    for name in files:
        if 'checkpoint' not in name:
            if 'jpg' in name:
                num_images = num_images + 1

attributes_dict = {}
vid_list = list(map(str,range(1, num_images+1)))
via3.dumpPrejects(vid_list)
via3.dumpConfigs()
via3.dumpAttributes(attributes_dict)
files_dict,  metadatas_dict = {},{}

#图片ID从1开始计算
image_id = 1

#循环遍历yolov5的检测标签
for root, dirs, files in os.walk(arg.yoloLabel_dir, topdown=False):
    for name in files:
        if 'txt' in name and 'checkpoint' not in name:

            #读取txt中的信息
            txtInfo=open(os.path.join(root, name))
            txtInfoLines = txtInfo.readlines() 
            
            #标注文件对应的图片
            tempImageName = name.split('.')[0] + '.jpg'
            files_dict[str(image_id)] = dict(fname=tempImageName, type=2)
            print("files_dict:",files_dict)
            
            img = cv2.imread(arg.image_dir+'/'+tempImageName)  #读取图片信息
            print(arg.image_dir+'/'+tempImageName)
            sp = img.shape #[高|宽|像素值由三种原色构成]
            img_H = sp[0]
            img_W = sp[1]
            for vid,txtInfoLine in enumerate(txtInfoLines,1):
                #只要身体的检测框
                if txtInfoLine.split(' ')[0] == '1':
                    txtInfoLineArr = txtInfoLine.split(' ')[1:5]
                    txtInfoLineArr[0] = float(txtInfoLineArr[0])
                    txtInfoLineArr[1] = float(txtInfoLineArr[1])
                    txtInfoLineArr[2] = float(txtInfoLineArr[2])
                    txtInfoLineArr[3] = float(txtInfoLineArr[3])
                    txtInfoLineArr = xywh2xyxy(txtInfoLineArr)
                    xyxy = txtInfoLineArr
                    xyxy[0] = img_W*txtInfoLineArr[0]
                    xyxy[2] = img_W*txtInfoLineArr[2]
                    xyxy[1] = img_H*txtInfoLineArr[1]
                    xyxy[3] = img_H*txtInfoLineArr[3]
                    temp_w = xyxy[2] - xyxy[0]
                    temp_h = xyxy[3] - xyxy[1]

                    metadata_dict = dict(vid=str(image_id),flg=0,z=[],
                                     xy=[2, float(xyxy[0]), float(xyxy[1]), float(temp_w), float(temp_h)],
                                     av={'1': '0'})
                    metadatas_dict['image{}_{}'.format(image_id,vid)] = metadata_dict

            image_id = image_id + 1 
            via3.dumpFiles(files_dict)
            via3.dumpMetedatas(metadatas_dict)
            
views_dict = {}
for i, vid in enumerate(vid_list,1):
    views_dict[vid] = defaultdict(list)
    views_dict[vid]['fid_list'].append(str(i))

via3.dumpViews(views_dict)
via3.dempJsonSave()
