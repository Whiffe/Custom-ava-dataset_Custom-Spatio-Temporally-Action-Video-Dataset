import sys
import os
import json
import pickle
import cv2  
import numpy as np
import codecs
import matplotlib.pyplot as plt
import argparse
import time

parser = argparse.ArgumentParser()

parser.add_argument('--label_dir', default='./chooseVideoFrameYolov5/exp/labels',type=str, help="Label path for yolov5")
parser.add_argument('--image_dir', default='./chooseVideoFrame/',type=str, help="Path of the image")
parser.add_argument('--newExp_dir', default='./chooseVideoFrameYolov5/newExp/',type=str, help="Label path after processing")
parser.add_argument('--visualize_dir', default='./visualize/',type=str, help="visualize path")
#labelPath = './chooseVideoFrameYolov5/exp/labels'
arg = parser.parse_args()

font = cv2.FONT_HERSHEY_COMPLEX_SMALL

#坐标格式转化 xywh代表：中心点与宽长，xyxy代表左上角点与右下角点
def xywhToxyxy(box):
    temp = box.copy()
    temp[0] = float(box[0]) - float(box[2]) / 2  # top left x
    temp[1] = float(box[1]) - float(box[3]) / 2  # top left y
    temp[2] = float(box[0]) + float(box[2]) / 2  # bottom right x
    temp[3] = float(box[1]) + float(box[3]) / 2  # bottom right y
    return temp

#可视化
def VisualizeBoxPlt(box1,box2,name1,name2,title, imgPath, saveImgPath):

    # 设置plt大小
    plt.rcParams['figure.figsize'] = (16.0, 16.0)
    
    img = cv2.imread(imgPath)
    #设置画布的大小
    sp = img.shape #[高|宽|像素值由三种原色构成]
    height = sp[0]
    width = sp[1]
    
    image = cv2.rectangle(img, (int(box1[0]*width),int(box1[1]*height)), (int(box1[2]*width),int(box1[3]*height)), (0,255,255), 2) 
    image = cv2.putText(img, name1, (int(box1[0]*width),int(box1[1]*height)+15), font, 1, (0, 0, 255), 1)
    image = cv2.rectangle(img, (int(box2[0]*width),int(box2[1]*height)), (int(box2[2]*width),int(box2[3]*height)), (0,255,0), 2) 
    image = cv2.putText(img, name2, (int(box2[2]*width),int(box2[3]*height)), font, 1, (0,255,0), 1)
    #image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    cv2.imwrite(saveImgPath, image)
    
def compareArea(box1,box2):
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    if box1_area <= box2_area:
        return 1
    else:
        return 0

#筛选出可能异常的检测框 ，通过算法检测后，确定为异常框，返回1
def filterAbnormalBox(headAr, abnormalBox,filename):
    for i,lineHead in enumerate(headAr):
        headBox = [float(lineHead[1]),float(lineHead[2]),float(lineHead[3]),float(lineHead[4])]
        headBox = xywhToxyxy(headBox)
    
        #在这里可视化，可以看到匹配全过程
        '''
        #可视化
        t = time.time()
        imgName = filename.split('.')[0]+'.jpg'
        newImgName = filename.split('.')[0]+ str(int(round(t * 1000000))) + '.jpg'
        VisualizeBoxPlt(headBox,abnormalBox,'headBox','abnormalBox','1 Find boxes that may be abnormal', arg.image_dir+imgName, arg.visualize_dir+newImgName)
        '''
        
        headBoxCenterX = (headBox[2] + headBox[0]) / 2
        headBoxCenterY = (headBox[1] + headBox[3]) / 2
        abnormalBoxCenterX = (abnormalBox[2] + abnormalBox[0]) / 2
        abnormalBoxCenterY = (abnormalBox[1] + abnormalBox[3]) / 2
    
        #筛选出没有交集的框
        if abs(headBoxCenterX - abnormalBoxCenterX) > (headBox[2]-headBox[0])/2 + (abnormalBox[2]-abnormalBox[0])/2 or abs(headBoxCenterY - abnormalBoxCenterY) > (headBox[3]-headBox[1])/2 + (abnormalBox[3]-abnormalBox[1])/2:
            #在这里可视化，可以看到筛选掉的框（两个框没有交集）
            '''
            #可视化
            t = time.time()
            imgName = filename.split('.')[0]+'.jpg'
            newImgName = filename.split('.')[0]+ str(int(round(t * 1000000))) + '.jpg'
            VisualizeBoxPlt(headBox,abnormalBox,'headBox','abnormalBox','1 Find boxes that may be abnormal', arg.image_dir+imgName, arg.visualize_dir+newImgName)
            '''
            continue
        #在这里可视化，可以看到有交集的框
        '''
        #可视化
        t = time.time()
        imgName = filename.split('.')[0]+'.jpg'
        newImgName = filename.split('.')[0]+ str(int(round(t * 1000000))) + '.jpg'
        VisualizeBoxPlt(headBox,abnormalBox,'headBox','abnormalBox','1 Find boxes that may be abnormal', arg.image_dir+imgName, arg.visualize_dir+newImgName)
        '''
        
        xi1 = max(headBox[0], abnormalBox[0])
        yi1 = max(headBox[1], abnormalBox[1])
        xi2 = min(headBox[2], abnormalBox[2])
        yi2 = min(headBox[3], abnormalBox[3])

        inter_area = (yi2 - yi1) * (xi2 - xi1)

        headBox_area = (headBox[2] - headBox[0]) * (headBox[3] - headBox[1])
        abnormalBox_area = (abnormalBox[2] - abnormalBox[0]) * (abnormalBox[3] - abnormalBox[1])

        min_box_area = min(headBox_area,abnormalBox_area)

        r_area = inter_area/min_box_area
        
        if r_area > 0.7:
            
            #在这里可视化，可以看到有交集重合度大于r_area的检测框
            '''
            #可视化
            t = time.time()
            imgName = filename.split('.')[0]+'.jpg'
            newImgName = filename.split('.')[0]+ str(int(round(t * 1000000))) + '.jpg'
            VisualizeBoxPlt(headBox,abnormalBox,'headBox','abnormalBox','1 Find boxes that may be abnormal', arg.image_dir+imgName, arg.visualize_dir+newImgName)
            '''
            
            
            r_area2 = headBox_area/abnormalBox_area

            if r_area2 > 0.5 and r_area2 < 1.5:
                
                #在这里可视化，可以看到有headBox_area与abnormalBox_area面积差距不能过大
                '''
                #可视化
                t = time.time()
                imgName = filename.split('.')[0]+'.jpg'
                newImgName = filename.split('.')[0]+ str(int(round(t * 1000000))) + '.jpg'
                VisualizeBoxPlt(headBox,abnormalBox,'headBox','abnormalBox','1 Find boxes that may be abnormal', arg.image_dir+imgName, arg.visualize_dir+newImgName)
                '''
                
                return 1
            
    return 0
            

def r_filter(box1, box2, headAr,filename):
    
    #在这里可视化，可以看到匹配全过程
    
    box1CenterX = (box1[2] + box1[0]) / 2
    box1CenterY = (box1[1] + box1[3]) / 2
    box2CenterX = (box2[2] + box2[0]) / 2
    box2CenterY = (box2[1] + box2[3]) / 2
    
    #筛选出没有交集的框
    if abs(box1CenterX - box2CenterX) > (box1[2]-box1[0])/2 + (box2[2]-box2[0])/2 or abs(box1CenterY - box2CenterY) > (box1[3]-box1[1])/2 + (box2[3]-box2[1])/2:
        #在这里可视化，可以看到筛选掉的框（两个框没有交集）
        return 0
       
    #在这里可视化，可以看到有交集的框
    '''
    #可视化
    t = time.time()
    imgName = filename.split('.')[0]+'.jpg'
    newImgName = filename.split('.')[0]+ str(int(round(t * 1000000))) + '.jpg'
    VisualizeBoxPlt(box1,box2,'box1','box2','1 Find boxes that may be abnormal', arg.image_dir+imgName, arg.visualize_dir+newImgName)
    '''
    
    xi1 = max(box1[0], box2[0])
    yi1 = max(box1[1], box2[1])
    xi2 = min(box1[2], box2[2])
    yi2 = min(box1[3], box2[3])
    
    inter_area = (yi2 - yi1) * (xi2 - xi1)
    
    if inter_area <= 0:
        return 0
    
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    
    min_box_area = min(box1_area,box2_area)
    
    r_area = inter_area/min_box_area
    
    boolHead = 0
    
    if r_area>0.7:   

        #在这里可视化，可以看到有交集重合度大于r_area的检测框
        '''
        #可视化
        t = time.time()
        imgName = filename.split('.')[0]+'.jpg'
        newImgName = filename.split('.')[0]+ str(int(round(t * 1000000))) + '.jpg'
        VisualizeBoxPlt(box1,box2,'box1','box2','1 Find boxes that may be abnormal', arg.image_dir+imgName, arg.visualize_dir+newImgName)
        '''
        
        if box1_area < box2_area:
            boolHead = filterAbnormalBox(headAr, box1,filename)
        else:
            return 0
        
    if boolHead == 0:
        return 0
    #在这里可视化，可以看到有交集重合度大于r_area的检测框
    '''
    #可视化
    t = time.time()
    imgName = filename.split('.')[0]+'.jpg'
    newImgName = filename.split('.')[0]+ str(int(round(t * 1000000))) + '.jpg'
    VisualizeBoxPlt(box1,box2,'box1','box2','1 Find boxes that may be abnormal', arg.image_dir+imgName, arg.visualize_dir+newImgName)
    '''
    return r_area

#计算总共筛选了多少个异常框
countAll = 0

# 需要筛选的检测标签数据位置
labelPath = arg.label_dir

print(labelPath)
for root, dirs, files in os.walk(labelPath):
    if root == labelPath:
        
        #排序，防止10排在1的前面
        files.sort(key=lambda arr: (int(arr[:-7]), int(arr[3:-4])))
        for filename in files:
            print(filename)
            #读取txt中的信息
            temp_txt=open(os.path.join(root, filename))
            temp_data_txt = temp_txt.readlines() 
            
            # 存放身体坐标与头部信息
            vbodyAr = []
            headAr = []
            
            #通过循环本次txt文件的坐标，取出头部与身体坐标
            for lineData in temp_data_txt:
                
                # 只要头的信息
                eLineData = lineData.split(' ')
                if eLineData[0]=='0':
                    headAr.append(eLineData)
                    
                # 只要身体的信息
                if eLineData[0]=='1':
                    vbodyAr.append(eLineData)
                    
            # 存放新txt文件
            new_data_txt = []
            
            #获取vbodyAr的长度
            lenVbodyAr = len(vbodyAr)
            s_count=0
            
            vbodyAr2 = vbodyAr.copy()
            # 再次循环，通过多层算法筛选，去掉异常检测框
            for i in range(lenVbodyAr):
                
                #delteE代表是否删除检测框，1代表删除，0代表不删除
                delteE = 0
                
                # 当前的检测框逐个对比其它检测框
                for j in range(i+1, lenVbodyAr, 1):
                    
                    box1 = []
                    box2 = []

                    #提取出两个检测框的坐标
                    box1 = [float(vbodyAr2[i][1]),float(vbodyAr2[i][2]),float(vbodyAr2[i][3]),float(vbodyAr2[i][4])]
                    box2 = [float(vbodyAr[j][1]),float(vbodyAr[j][2]),float(vbodyAr[j][3]),float(vbodyAr[j][4])]

                    #坐标格式转化
                    box1 = xywhToxyxy(box1)
                    box2 = xywhToxyxy(box2)

                    filter = r_filter(box1,box2,headAr,filename)
                    
                    if filter > 0.7:
                        s_count = s_count+1


                        dirImage = arg.image_dir
                        dirFile = filename.split('_')[0]
                        dirFileName = filename.split('.')[0]+'.jpg'
                        path = dirImage + dirFile + '/' + dirFileName

                        # 当box1的面积小于等于box2时，该坐标就该删除了
                        if compareArea(box1,box2) == 1:
                            delteE = 1
                            # 可视化
                            #VisualizeBoxPlt(box1,box2,'box1','box2','4 Visualize the results of a successful filter', imgTag=True, path = path)
                            countAll = countAll + 1
                            break


                if delteE == 0:
                    new_data_txt.append(vbodyAr2[i][0])
                    new_data_txt.append(" ")
                    new_data_txt.append(vbodyAr2[i][1])
                    new_data_txt.append(" ")
                    new_data_txt.append(vbodyAr2[i][2])
                    new_data_txt.append(" ")
                    new_data_txt.append(vbodyAr2[i][3])
                    new_data_txt.append(" ")
                    new_data_txt.append(vbodyAr2[i][4])
                    new_data_txt.append(" ")
                    new_data_txt.append(vbodyAr2[i][5]) 
            print("new:",len(new_data_txt))
            print("old:",len(vbodyAr))
            
            newExp = arg.newExp_dir
            newExpDir = newExp + filename
            
            f = codecs.open(newExpDir,'w')

            for i in new_data_txt:
                f.write(str(i)) 
            f.close()

print("countAll:",countAll)
