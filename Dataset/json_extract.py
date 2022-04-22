import json
import os
import csv
import cv2

# dict存放最后的json
dicts = []
# 通过循环与判断来找出via的json标注文件
for root, dirs, files in os.walk("./choose_frames_middle", topdown=False):
    for file in files:
        #via的json标注文件以_proposal.json结尾
        if "_finish.json" in file:
            jsonPath = root+'/'+file
            index = 0
            #读取标注文件
            with open(jsonPath, encoding='utf-8') as f:
                line = f.readline()
                viaJson = json.loads(line)
                
                
                attributeNum1 = len(viaJson['attribute']['1']['options'])
                attributeNum2 = len(viaJson['attribute']['2']['options'])+attributeNum1
                #attributeNum3 = len(viaJson['attribute']['3']['options'])+attributeNum2
                attributeNums = [0,attributeNum1,attributeNum2]
                
                files = {}
                for file in viaJson['file']:
                    fid = viaJson['file'][file]['fid']
                    fname = viaJson['file'][file]['fname']
                    files[fid]=fname
                for metadata in viaJson['metadata']:
                    imagen_x = viaJson['metadata'][metadata]
                    #获取人的坐标
                    xy = imagen_x['xy'][1:]
                    #获取vid，目的是让坐标信息与图片名称、视频名称对应
                    vid = imagen_x['vid']
                    fname = files[vid]
                    #获取视频名称
                    videoName = fname.split('_')[0]
                    #获取视频帧ID
                    frameId = int((int(fname.split('_')[1].split('.')[0])-1)/30)
                    for action in imagen_x['av']:
                        avs = imagen_x['av'][action]
                        #行为复选框不为空,获取复选框中的行为
                        if avs != '':
                            #一个复选框可能有多个选择
                            avArr = avs.split(',')
                            for av in avArr:
                                
                                # 获取坐标对应的图片，因为最后的坐标值需要在0到1
                                # 就需要用现有坐标值/图片大小
                                imgPath = root + '/' + videoName + "_" + str(frameId*30+1).zfill(6) + '.jpg'
                                imgTemp = cv2.imread(imgPath)  #读取图片信息
                                print(imgPath)
                                sp = imgTemp.shape #[高|宽|像素值由三种原色构成]
                                img_H = sp[0]
                                img_W = sp[1]
                                x1 = xy[0] / img_W
                                y1 = xy[1] / img_H
                                x2 = (xy[0]+xy[2]) / img_W
                                y2 = (xy[1]+xy[3]) / img_H
                                
                                # 防止坐标点超过图片大小
                                if x1 < 0:
                                    x1 = 0
                                if x1 > 1:
                                    x1 = 1
                                    
                                if x2 < 0:
                                    x2 = 0
                                if x2 > 1:
                                    x2 = 1
                                    
                                if y1 < 0:
                                    y1 = 0
                                if y1 > 1:
                                    y1 = 1
                                    
                                if y2 < 0:
                                    y2 = 0
                                if y2 > 1:
                                    y2 = 1
                                
                                actionId = attributeNums[int(action)-1]+int(av)+1
                                dict = [videoName,frameId,x1,y1,x2,y2,actionId]
                                
                                
                                dicts.append(dict)
                    index = index + 1
with open('./train_without_personID.csv',"w") as csvfile: 
    writer = csv.writer(csvfile)
    writer.writerows(dicts)

