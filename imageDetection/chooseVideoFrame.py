import os
import shutil
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--seconds', default=15,type=int, help="Length of video, seconds")
parser.add_argument('--frames_dir', default='../Dataset/frames',type=str, help="The path of all video frames")
parser.add_argument('--chooseFrame_dir', default='./chooseVideoFrame/',type=str, help="The path where the selected image is stored")

arg = parser.parse_args()

#如果chooseFrame_dir对应的目录不存在，则创建
if not os.path.exists(arg.chooseFrame_dir):
    os.mkdir(arg.chooseFrame_dir)

#选取视频中间的一帧
chooseSecond = int(arg.seconds/2)

# 需要检测标注的时间位置[0,1,2,3,4,5,6,7,8,9,10]
frames = range(0, arg.seconds+1)

# num_frames 存放对应图片的编号
num_frames = []

for i in frames:
    num_frames.append(i*30+1)
#遍历./frames
for filepath,dirnames,filenames in os.walk(arg.frames_dir):
    filenames=sorted(filenames)
    for filename in filenames:
        if str(chooseSecond*30+1) in filename:
            srcfile = filepath + '/' + filename
            dstpath = arg.chooseFrame_dir + filename
            # 复制文件
            shutil.copy(srcfile, dstpath)
            print(filename)
        
