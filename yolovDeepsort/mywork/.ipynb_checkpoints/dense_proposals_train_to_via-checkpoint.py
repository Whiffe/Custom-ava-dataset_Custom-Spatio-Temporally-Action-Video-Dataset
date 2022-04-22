from via3_tool import Via3Json
import pickle
import csv
from collections import defaultdict
import os
import cv2
import sys

#传参 ./avaMin_dense_proposals_train.pkl
avaMin_dense_proposals_path = sys.argv[1]

#传参 ../videoData/choose_frames/
json_path = sys.argv[2]


f = open(avaMin_dense_proposals_path,'rb')
info = pickle.load(f, encoding='iso-8859-1') 



attributes_dict = {'1':dict(aname='head', type=2, options={'0':'talk',
                   '1':'bow'},default_option_id="", anchor_id = 'FILE1_Z0_XY1'),

                   '2': dict(aname='body', type=2, options={'0':'stand',
                   '1':'sit', '2':'walk'}, default_option_id="", anchor_id='FILE1_Z0_XY1'),
                   
                  '3':dict(aname='limbs', type=2, options={'0':'hand up',
                   '1':'catch'},default_option_id="", anchor_id = 'FILE1_Z0_XY1'),
                  }

#len_x与循环的作用主要是获取每个视频下视频帧的数量
dirname = ''
len_x = {}
for i in info:
    temp_dirname = i.split(',')[0]
    if dirname == temp_dirname:
        #正在循环一个视频文件里的东西
        len_x[dirname] = len_x[dirname] + 1
    else:
        #进入下一个视频文件
        dirname = temp_dirname
        len_x[dirname] = 1

dirname = ''
for i in info:
    temp_dirname = i.split(',')[0]
    if dirname == temp_dirname:
        #正在循环一个视频文件里的东西
    
        #图片ID从1开始计算
        image_id = image_id + 1
        files_img_num = int(i.split(',')[1])
        
        # 如果当前出现 files_img_num - 1 与 image_id 不相等的情况
        # 那就代表当前 image_id对应的图片中没有人
        # 那么via的标注记为空
        if files_img_num - 1 != image_id:
            files_dict[str(image_id)] = dict(fname=i.split(',')[0] + '_' + (str((image_id+1)*30+1)).zfill(6) + '.jpg', type=2)
            via3.dumpFiles(files_dict)
            if files_img_num - 1 != image_id:
                while image_id < files_img_num - 1:   
                    image_id = image_id + 1
                    files_dict[str(image_id)] = dict(fname=i.split(',')[0] + '_' + (str((image_id+1)*30+1)).zfill(6) + '.jpg', type=2)
                    via3.dumpFiles(files_dict)
                    print("middle loss",image_id,"   ",num_images)
                    print("files_img_num-1",files_img_num-1," image_id",image_id)
                    len_x[dirname] = len_x[dirname] + 1
                    continue

        files_dict[str(image_id)] = dict(fname=i.split(',')[0] + '_' + (str(int(i.split(',')[1])*30+1)).zfill(6) + '.jpg', type=2)
        
        for vid,result in enumerate(info[i],1):
            xyxy = result
            xyxy[0] = img_W*xyxy[0]
            xyxy[2] = img_W*xyxy[2]
            xyxy[1] = img_H*xyxy[1]
            xyxy[3] = img_H*xyxy[3]
            temp_w = xyxy[2] - xyxy[0]
            temp_h = xyxy[3] - xyxy[1]
            
            metadata_dict = dict(vid=str(image_id),
                                 xy=[2, float(xyxy[0]), float(xyxy[1]), float(temp_w), float(temp_h)],
                                 av={'1': '0'})
            
            metadatas_dict['image{}_{}'.format(image_id,vid)] = metadata_dict
        
        via3.dumpFiles(files_dict)
        via3.dumpMetedatas(metadatas_dict)
        
        print("OK ",image_id,"   ",num_images)
        if image_id == num_images:
            views_dict = {}
            for i, vid in enumerate(vid_list,1):
                views_dict[vid] = defaultdict(list)
                views_dict[vid]['fid_list'].append(str(i))
            via3.dumpViews(views_dict)
            via3.dempJsonSave()
            print("save")
        
        #当一个视频的图片的标注信息遍历完后：image_id == len_x[dirname]，
        #但是视频的标注信息长度仍然小于视频实际图片长度
        #即视频图片最后几张都是没有人，导致视频标注信息最后几张没有
        #那么就执行下面的语句，给最后几张图片添加空的标注信息
        print("image_id",image_id," len_x[dirname]",len_x[dirname]," num_images",num_images)
        if image_id == len_x[dirname] and image_id < num_images:
            while image_id < num_images:
                image_id = image_id + 1
                files_dict[str(image_id)] = dict(fname=i.split(',')[0] + '_' + (str((image_id+1)*30+1)).zfill(6) + '.jpg', type=2)
                via3.dumpFiles(files_dict)
            print("end loss",image_id,"   ",num_images)
            views_dict = {}
            for i, vid in enumerate(vid_list,1):
                views_dict[vid] = defaultdict(list)
                views_dict[vid]['fid_list'].append(str(i))
            via3.dumpViews(views_dict)
            via3.dempJsonSave()
            print("save")
    else:
        #进入下一个视频文件
        dirname = temp_dirname
        print("dirname",dirname)
        
        #为每一个视频文件创建一个via的json文件
        temp_json_path = json_path + dirname + '/' + dirname + '_proposal.json'
        
        # 获取视频有多少个帧
        for root, dirs, files in os.walk(json_path + dirname, topdown=False):
            if "ipynb_checkpoints" in root:
                continue
            num_images = 0
            for file in files:
                if '.jpg' in file:
                    num_images = num_images + 1
                    temp_img_path = json_path + dirname +'/' + file #图片路径
                    img = cv2.imread(temp_img_path)  #读取图片信息
                    sp = img.shape #[高|宽|像素值由三种原色构成]
                    img_H = sp[0]
                    img_W = sp[1]
        via3 = Via3Json(temp_json_path, mode='dump')
        vid_list = list(map(str,range(1, num_images+1)))
        via3.dumpPrejects(vid_list)
        via3.dumpConfigs()
        via3.dumpAttributes(attributes_dict)
        
        
        files_dict,  metadatas_dict = {},{}
        #图片ID从1开始计算
        image_id = 1
        files_dict[str(image_id)] = dict(fname=i.split(',')[0] + '_' + (str(int(i.split(',')[1])*30+1)).zfill(6) + '.jpg', type=2)
        
        for vid,result in enumerate(info[i],1):
            xyxy = result
            xyxy[0] = img_W*xyxy[0]
            xyxy[2] = img_W*xyxy[2]
            xyxy[1] = img_H*xyxy[1]
            xyxy[3] = img_H*xyxy[3]
            temp_w = xyxy[2] - xyxy[0]
            temp_h = xyxy[3] - xyxy[1]
            
            metadata_dict = dict(vid=str(image_id),
                                 xy=[2, float(xyxy[0]), float(xyxy[1]), float(temp_w), float(temp_h)],
                                 av={'1': '0'})
            #print(metadata_dict)
            metadatas_dict['image{}_{}'.format(image_id,vid)] = metadata_dict
        
        via3.dumpFiles(files_dict)
        via3.dumpMetedatas(metadatas_dict)