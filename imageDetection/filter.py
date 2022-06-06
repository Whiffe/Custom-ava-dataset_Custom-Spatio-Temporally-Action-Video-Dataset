import sys
import os
import json
import pickle
import cv2  
import numpy as np
import codecs
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--label_dir', default='./chooseVideoFrameYolov5/exp/labels',type=str, help="Label path for yolov5")
parser.add_argument('--image_dir', default='./chooseVideoFrame/',type=str, help="Path of the image")
parser.add_argument('--newExp_dir', default='./chooseVideoFrameYolov5/newExp/',type=str, help="Label path after processing")
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
def VisualizeBoxPlt(box1,box2,name1,name2,title, imgTag=False, path = ''):
    
    # 设置plt大小
    plt.rcParams['figure.figsize'] = (16.0, 16.0)
    
    #设置画布的大小
    width = 1920
    height = 1080
    if imgTag:
        img = cv2.imread(path)
        
    else:
        img = np.zeros((height, width, 3), np.uint8)
    
    image = cv2.rectangle(img, (int(box1[0]*width),int(box1[1]*height)), (int(box1[2]*width),int(box1[3]*height)), (0,0,255), 4) 
    image = cv2.putText(img, name1, (int(box1[0]*width),int(box1[1]*height)+15), font, 2, (0, 0, 255), 2)
    image = cv2.rectangle(img, (int(box2[0]*width),int(box2[1]*height)), (int(box2[2]*width),int(box2[3]*height)), (0,255,0), 4) 
    image = cv2.putText(img, name2, (int(box2[2]*width),int(box2[3]*height)), font, 2, (0,255,0), 2)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.title(title)
    plt.imshow(image)
    plt.show()
    plt.close()
    
    
def compareArea(box1,box2):
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    if box1_area <= box2_area:
        return 1
    else:
        return 0

#筛选出可能异常的检测框 ，通过算法检测后，确定为异常框，返回1
def filterAbnormalBox(headAr, abnormalBox):
    for i,lineHead in enumerate(headAr):
        headBox = [float(lineHead[1]),float(lineHead[2]),float(lineHead[3]),float(lineHead[4])]
        headBox = xywhToxyxy(headBox)

        # 下面四个if判断是去除没有交集的box
        if abs(headBox[0] - abnormalBox[0]) > max(headBox[2]-headBox[0],abnormalBox[2]-abnormalBox[0]) :
            continue
        if abs(headBox[1] - abnormalBox[1]) > max(headBox[3]-headBox[1],abnormalBox[3]-abnormalBox[1]) :
            continue
        if abs(headBox[2] - abnormalBox[2]) > max(headBox[2]-headBox[0],abnormalBox[2]-abnormalBox[0]) :    
            continue
        if abs(headBox[3] - abnormalBox[3]) >  max(headBox[3]-headBox[1],abnormalBox[3]-abnormalBox[1]) :
            continue

        xi1 = max(headBox[0], abnormalBox[0])
        yi1 = max(headBox[1], abnormalBox[1])
        xi2 = min(headBox[2], abnormalBox[2])
        yi2 = min(headBox[3], abnormalBox[3])

        inter_area = (yi2 - yi1) * (xi2 - xi1)

        if inter_area <= 0:
            continue

        headBox_area = (headBox[2] - headBox[0]) * (headBox[3] - headBox[1])
        abnormalBox_area = (abnormalBox[2] - abnormalBox[0]) * (abnormalBox[3] - abnormalBox[1])

        min_box_area = min(headBox_area,abnormalBox_area)

        r_area = inter_area/min_box_area
                
        #可视化
        #VisualizeBoxPlt(headBox,abnormalBox,'headBox','abnormalBox','2 The headBox around the abnormalBox')
        
        if r_area > 0.4:
            
            r_area2 = headBox_area/abnormalBox_area

            if r_area2 > 0.5 and r_area2 < 1.5:
                
                #可视化
                #VisualizeBoxPlt(headBox,abnormalBox,'headBox','abnormalBox','3 Determine the filter abnormalBox')
                
                return 1
            
    return 0
            

def r_filter(box1, box2, headAr):
    
    # 下面四个if判断是去除没有交集的box
    if abs(box1[0] - box2[0]) > max(box1[2]-box1[0],box2[2]-box2[0]) :
        return 0
    if abs(box1[1] - box2[1]) > max(box1[3]-box1[1],box2[3]-box2[1]) :
        return 0
    if abs(box1[2] - box2[2]) > max(box1[2]-box1[0],box2[2]-box2[0]) :    
        return 0
    if abs(box1[3] - box2[3]) >  max(box1[3]-box1[1],box2[3]-box2[1]) :
        return 0
    
    # 只留下有包含关系的box中：其中一个box位于另一个box的顶部!，顶部！
    #if abs(box1[1] - box2[1]) > max(box1[3]-box1[1],box2[3]-box2[1])*0.4:
    #    return 0
    
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
    
    if min_box_area <= inter_area:
        return 0
    
    r_area = inter_area/min_box_area
    
    boolHead = 0
    
    
    
    
    if r_area>0.7:      
        
        #可视化
        #VisualizeBoxPlt(box1,box2,'box1','box2','1 Find boxes that may be abnormal')
        
        if box1_area < box2_area:
            boolHead = filterAbnormalBox(headAr, box1)
        else:
            boolHead = filterAbnormalBox(headAr, box2)
        
    if boolHead == 0:
        return 0
    
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
                
                # 只要人的信息
                eLineData = lineData.split(' ')
                if eLineData[0]=='0':
                    headAr.append(eLineData)
                    
                # 只要头的信息
                if eLineData[0]=='1':
                    vbodyAr.append(eLineData)
                    
            # 存放新txt文件
            new_data_txt = []
            
            #获取vbodyAr的长度
            lenB = len(vbodyAr)
            s_count=0
            
            # 再次循环，通过多层算法筛选，去掉异常检测框
            for i,lineData in enumerate(temp_data_txt):
                
                #delteE代表是否删除检测框，1代表删除，0代表不删除
                delteE = 0
                
                # 当前的检测框逐个对比其它检测框
                for j in range(i+1, lenB, 1):
                    
                    box1 = []
                    box2 = []
                    eLineData = lineData.split(' ')
                    
                    # 只进行身体检测框的筛选
                    if eLineData[0]=='1':
                        
                        #提取出两个检测框的坐标
                        box1 = [float(eLineData[1]),float(eLineData[2]),float(eLineData[3]),float(eLineData[4])]
                        box2 = [float(vbodyAr[j][1]),float(vbodyAr[j][2]),float(vbodyAr[j][3]),float(vbodyAr[j][4])]
                        
                        #坐标格式转化
                        xywhToxyxy(box1)
                        xywhToxyxy(box2)
                        
                        filter = r_filter(box1,box2,headAr)
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
                    new_data_txt.append(lineData) 
            print("new:",len(new_data_txt))
            print("old:",len(temp_data_txt))
            
            newExp = arg.newExp_dir
            newExpDir = newExp + filename
            
            f = codecs.open(newExpDir,'w')

            for i in new_data_txt:
                f.write(str(i)) 
            f.close()

print("countAll:",countAll)
