import os
import shutil
import sys

#遍历./frames
for filepath,dirnames,filenames in os.walk(r'./choose_frames'):
    if len(filenames) == 0:
        continue
    
    #在choose_frames下创建对应的目录文件夹
    temp_name = filepath.split('/')[-1]
    path_temp_name = './choose_frames_middle/'+temp_name
    if not os.path.exists(path_temp_name):
        os.makedirs(path_temp_name)
        print(path_temp_name)
    filenames=sorted(filenames)
    #找到指定的图片，然后移动到choose_frames中对应的文件夹下
    for filename in filenames:
        if "checkpoint" in filename:
            continue
        temp_num = filename.split('_')[1]
        temp_num = temp_num.split('.')[0]
        temp_num = int(temp_num)
        
        if (temp_num-1)/30 <= 1 or (temp_num-1)/30 >= len(filenames) - 2:
            continue
        temp_num = str(temp_num)
        temp_num = temp_num.zfill(6)
        temp_num = temp_name + "_" + temp_num + ".jpg"

        srcfile = filepath + '/' + temp_num
        dstpath = path_temp_name + '/' + temp_num
        # 复制文件
        shutil.copy(srcfile, dstpath)
        #print(dstpath)