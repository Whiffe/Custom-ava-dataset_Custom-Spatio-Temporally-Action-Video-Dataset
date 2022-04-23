import os
import shutil
import sys

#传参 这里传入视频多少秒
seconds = int(sys.argv[1])

#传参 这里传入视频从那一秒开始，这里需要设置为 0
start = int(sys.argv[2])

# 需要检测标注的时间位置[0,1,2,3,4,5,6,7,8,9,10]
frames = range(start, seconds+1)

# num_frames 存放对应图片的编号
num_frames = []

for i in frames:
    num_frames.append(i*30+1)

#遍历./frames
for filepath,dirnames,filenames in os.walk(r'./frames'):
    #在choose_frames下创建对应的目录文件夹
    if len(filenames)!=0:
        temp_name = filepath.split('/')[-1]
        path_temp_name = './choose_frames/'+temp_name
        if not os.path.exists(path_temp_name):
            os.makedirs(path_temp_name)
    filenames=sorted(filenames)
    #找到指定的图片，然后移动到choose_frames中对应的文件夹下
    for filename in filenames:
        if "checkpoint" in filename:
            continue
        if "Store" in filename:
            continue
        temp_num = filename.split('_')[1]
        temp_num = temp_num.split('.')[0]
        temp_num = int(temp_num)
        if temp_num in num_frames:
            temp_num = str(temp_num)
            temp_num = temp_num.zfill(6)
            temp_num = temp_name + "_" + temp_num + ".jpg"
            
            srcfile = filepath + '/' + temp_num
            dstpath = path_temp_name + '/' + temp_num
            # 复制文件
            shutil.copy(srcfile, dstpath)
