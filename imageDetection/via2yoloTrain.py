import json
import cv2
import os
import random
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--anno_dir', default='./chooseVideoFrame/detection2.json',type=str, help="anno_dir is the annotation file after relabeling")
parser.add_argument('--img_dir', default='./chooseVideoFrame/',type=str, help="img_dir is the image position")
parser.add_argument('--newLabels_dir', default='./chooseVideoFrameYolov5/yolov5CusDataset/labels/',type=str, help="newLabelsPath is the storage for: the re-labeled ( detection2.json) file of via, the refactored multiple txt")
parser.add_argument('--newImages_dir', default='./chooseVideoFrameYolov5/yolov5CusDataset/images/',type=str, help="newImagesPath is the location where the image will be repositioned")

# 训练：测试：验证=6:2:2
ratio_train=0.8
ratio_test=0.1
ratio_val=0.1

randomChoose = {}

#清空即将创建的数据集可能存在的数据
os.system('rm -r ./chooseVideoFrameYolov5/yolov5CusDataset/images/train/*')
os.system('rm -r ./chooseVideoFrameYolov5/yolov5CusDataset/images/test/*')
os.system('rm -r ./chooseVideoFrameYolov5/yolov5CusDataset/images/val/*')
os.system('rm -r ./chooseVideoFrameYolov5/yolov5CusDataset/labels/train/*')
os.system('rm -r ./chooseVideoFrameYolov5/yolov5CusDataset/labels/test/*')
os.system('rm -r ./chooseVideoFrameYolov5/yolov5CusDataset/labels/val/*')

for root, dirs, files in os.walk(arg.img_dir, topdown=False):
    for name in files:
        if '.jpg' in name and 'checkpoint' not in name:
            randNum = random.random()
            #随机选择train、test、val所对应的图片名称，并将图片复制到对应的文件夹中
            if randNum <= ratio_train:
                randomChoose[name.split('.')[0]]='train'
                os.system('cp ' + arg.img_dir + name + ' ' + arg.newImages_dir + 'train/' + name)
            if randNum > ratio_train and randNum <= ratio_train + ratio_test:
                randomChoose[name.split('.')[0]]='test'
                os.system('cp ' + arg.img_dir + name + ' ' + arg.newImages_dir + 'test/' + name)
            if randNum > ratio_train + ratio_test:
                randomChoose[name.split('.')[0]]='val'
                os.system('cp ' + arg.img_dir + name + ' ' + arg.newImages_dir + 'val/' + name)

#加载标注文件
ann = json.load(open(arg.anno_dir))

for img_id, key in enumerate(ann['file']):
    fname = ann['file'][key]['fname']
    metadata = ann['metadata']
    # txtArr存放一张图片中的标注信息
    txtArr = ''
    for image in metadata:
        # imageId 的作用是让图片与标注信息匹配，一张图片对应多个标注信息，让每一张图片的标注信息合成在一个txt中
        imageId = image.split('_')[0][-1]
        if imageId == key:
            img = cv2.imread(arg.img_dir+'/'+fname)  #读取图片信息
            sp = img.shape #[高|宽|像素值由三种原色构成]
            img_H = sp[0]
            img_W = sp[1]
            xywh = ann['metadata'][image]['xy'][1:]
            YoloXywh = xywh.copy()
            YoloXywh[3] = xywh[3]/img_H
            YoloXywh[2] = xywh[2]/img_W
            YoloXywh[1] = (xywh[1]+xywh[3]/2)/img_H
            YoloXywh[0] = (xywh[0]+xywh[2]/2)/img_W
            txtArr = txtArr + '0 ' + str(YoloXywh[0]) + ' ' + str(YoloXywh[1]) + ' ' + str(YoloXywh[2]) + ' ' + str(YoloXywh[3]) + '\n' 
    #去除最后一行（多了个回车）
    txtArr = txtArr[:-2]
    #将txt保存到对应的train、val、test目录下
    txtPath = arg.newLabels_dir + randomChoose[fname.split('.')[0]]+'/'+fname.split('.')[0]+'.txt'
    print("txtPath:",txtPath)
    with open(txtPath,"w") as f:
        f.write(txtArr)  # 自带文件关闭功能，不需要再写f.close()

