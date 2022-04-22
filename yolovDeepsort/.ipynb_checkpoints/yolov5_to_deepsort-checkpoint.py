import argparse
import sys
import csv
#sys.path.append('..') #目的是为了导入上一级的yolov5
sys.path.insert(0, './yolov5/')

from yolov5.utils.datasets import LoadImages
from yolov5.utils.general import check_img_size,xyxy2xywh
from deep_sort_pytorch.utils.parser import get_config
from deep_sort_pytorch.deep_sort import DeepSort

import cv2
import torch
import numpy as np
import torch.backends.cudnn as cudnn
import pickle
from PIL import Image

#python yolov5_to_deepsort.py --source ../videoData/frames/

# dict存放最后的json
dicts = []
def detect(opt):
    source = opt.source
    stride = 32
    pt = True
    jit = False
    
    
    cfg = get_config()
    cfg.merge_from_file(opt.config_deepsort)
    
    # 这里是avaMin_dense_proposals_train.pkl的路径，
    # 但是之后要使用via标注之后的avaMin_train.csv，因为在微调之后，坐标数量与坐标位置会发生变化
    f = open('./mywork/dense_proposals_train_deepsort.pkl','rb')
    info = pickle.load(f, encoding='iso-8859-1') 
    
    # tempFileName 用以记录当前所处文件（或者视频），如果读取到下一个文
    # 件（或者视频），则tempFileName更换为下一个文件名，然后deepsort重新开始检测
    tempFileName = ''
    
    # 循环 pkl中的信息
    for i in info:
        dets = info[i]
        tempName = i.split(',')
        
        # 如果新开启一个文件（或者视频），deepsort重写开始检测
        if tempName[0] != tempFileName:
            deepsort = DeepSort(cfg.DEEPSORT.REID_CKPT,
                        max_dist=cfg.DEEPSORT.MAX_DIST, min_confidence=cfg.DEEPSORT.MIN_CONFIDENCE,
                        max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                        max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                        use_cuda=True)
            tempFileName = tempName[0]
        
        # 读取当前标注信息所对应的图片
        tempImg = cv2.imread(source + '/' + tempName[0] + '/' +tempName[0]+'_'+str(int(tempName[1])*30+1).zfill(6) + '.jpg') 
        # 获取图片的大小
        imgsz = tempImg.shape
        
        # pkl中的的坐标是左上角与右下角，即xyxy，
        # 但是输入到deepsort中的值是人的中心坐标与长宽，注意是中心坐标，即xywh
        xyxys = torch.FloatTensor(len(dets), 4)
        confs = torch.FloatTensor(len(dets))
        clss = torch.FloatTensor(len(dets))
        for index, det in enumerate(dets):
            xyxys[index][0]=det[0]*imgsz[1]
            xyxys[index][1]=det[1]*imgsz[0]
            xyxys[index][2]=det[2]*imgsz[1]
            xyxys[index][3]=det[3]*imgsz[0]
            confs[index]=(float(det[4]))
            clss[index]=0.
            
        xywhs = xyxy2xywh(xyxys)
        
        # 由于标注信息是每隔 30帧检测一次，导致送入deep sort的检测数量减少
        # 所以增加送入deep sort的帧
        # 增加策略：讲当前帧的前面第10帧与后面第10帧送入检测，
        # 即送入：当前帧-10，当前帧，当前帧+10 
        '''
        im0Path = source + '/' + tempName[0] + '/'+ tempName[0] + '_' + str(int(tempName[1])*30+1).zfill(6) + '.jpg'
        im0 = np.array(Image.open(im0Path))
        
        im0sub10Path = source + '/' + tempName[0] + '/' + tempName[0] + '_' + str(int(tempName[1])*30-9).zfill(6) + '.jpg'
        im0sub10 = np.array(Image.open(im0sub10Path))
        
        im0add10Path = source + '/' + tempName[0] + '/' + tempName[0] + '_' + str(int(tempName[1])*30 + 9).zfill(6) + '.jpg'
        im0add10 = np.array(Image.open(im0add10Path))
        
        print("xywhs:",xywhs)
        outputs = deepsort.update(xywhs, confs, clss, im0sub10)
        print("outputs1",outputs)
        outputs = deepsort.update(xywhs, confs, clss, im0)
        print("outputs2",outputs)
        outputs = deepsort.update(xywhs, confs, clss, im0add10)
        print("outputs3",outputs)
        print("im0sub10Path",im0sub10Path)
        input()
        '''
        im0Path = source + '/' + tempName[0] + '/'+ tempName[0] + '_' + str(int(tempName[1])*30+1).zfill(6) + '.jpg'
        im0 = np.array(Image.open(im0Path))
        outputs = deepsort.update(xywhs, confs, clss, im0)
        
        # 这里存在一个问题，len(outputs)可能会小于len(xywhs)
        # 原因是某些人在视频中首次出现（第二秒后首次出现）
        # deepsort对其检测将不会输出结果
        # 当该人出现在检测图片中第三次后，才会有检测结果。
        # outputs[0],outputs[1],outputs[2],outputs[3] 代表坐标
        # outputs[4]代表ID
        if len(outputs) > 0:
            for output in outputs:
                x1 = output[0]/ imgsz[1]
                y1 = output[1]/ imgsz[0]
                x2 = output[2]/ imgsz[1]
                y2 = output[3]/ imgsz[0]
                dict = [tempName[0],tempName[1],x1,y1,x2,y2,output[4]]
                dicts.append(dict)
        with open('../videoData/ava_train_personID.csv',"w") as csvfile: 
            writer = csv.writer(csvfile)
            writer.writerows(dicts)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--deep_sort_weights', type=str, default='deep_sort_pytorch/deep_sort/deep/checkpoint/ckpt.t7', help='ckpt.t7 path')
    # file/folder, 0 for webcam
    parser.add_argument('--source', type=str, default='0', help='source')
    #parser.add_argument('--output', type=str, default='inference/output', help='output folder')  # output folder
    parser.add_argument('--save-txt', action='store_true', help='save MOT compliant results to *.txt')
    # class 0 is person, 1 is bycicle, 2 is car... 79 is oven
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 16 17')
    
    parser.add_argument("--config_deepsort", type=str, default="deep_sort_pytorch/configs/deep_sort.yaml")
    
    opt = parser.parse_args()
    with torch.no_grad():
        detect(opt)