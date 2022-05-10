import sys
import os
import json
import pickle

#传参 labelPath是yolov5检测结果的位置，需要获取0（0代表人）的四个坐标值，还需要检测概率
# ../yolov5/runs/detect/exp/labels
labelPath = sys.argv[1]

#传参 保存为pkl的地址，这是像ava数据集对齐
# ./avaMin_dense_proposals_train.pkl
avaMin_dense_proposals_path = sys.argv[2]

#传参 是否可视化
#可见就传入 show，否则不填
showPkl = sys.argv[3]

results_dict = {}
dicts = []
for root, dirs, files in os.walk(labelPath):
    lenFile = len(files)/3
    if root == labelPath:
        #排序，防止10排在1的前面
        files.sort(key=lambda arr: (int(arr[:-7]), int(arr[3:-4])))
        for name in files:
            temp_file_name = name.split("_")[0]
            temp_video_ID = name.split("_")[1].split('.')[0]
            temp_video_ID = int(temp_video_ID)
            temp_video_ID = str(int((temp_video_ID-1)/30))
            temp_video_ID = temp_video_ID.zfill(4)
            
            # 这里的 if 判断，目的是去掉 开始的 2 个，与结尾的 2 个
            if int(temp_video_ID) <= 1 or int(temp_video_ID) >= lenFile:
                continue
            
            # key = '视频名字,第几秒的视频' 如 '1,0002'，代表视频1的第2秒
            key = temp_file_name + ',' + temp_video_ID
            
            #读取yolov5中的信息
            temp_txt=open(os.path.join(root, name))
            temp_data_txt = temp_txt.readlines() 
            results = []
            for i in temp_data_txt:
                # 只要人的信息
                j = i.split(' ')
                if j[0]=='1':
            
                    # 由于yolov5的检测结果是 xywh
                    # 要将xywh转化成xyxy
                    y = j
                    y[1] = float(j[1]) - float(j[3]) / 2  # top left x
                    y[2] = float(j[2]) - float(j[4]) / 2  # top left y
                    y[3] = float(j[1]) + float(j[3])  # bottom right x
                    y[4] = float(j[2]) + float(j[4])  # bottom right y
                    
                    results.append([y[1],y[2],y[3],y[4],y[5]])
                    temp_txt.close()  # 关闭文件
                    dicts.append([y[1],y[2],y[3],y[4],y[5]])
            results_dict[key] = results

# 保存为pkl文件
with open(avaMin_dense_proposals_path,"wb") as pklfile: 
    pickle.dump(results_dict, pklfile)
    
# 显示pkl文件中的内容
if showPkl == "show":
    for i in results_dict:
        print(i,results_dict[i])
        #input()
