import os
import shutil
import sys

#这里输入视频有多少秒
#seconds = 180
#传参 这里传入视频多少秒
seconds = int(sys.argv[1])

#选取视频中间的一帧
chooseSecond = int(seconds/2)

# 默认从第二秒开始检测标注
# start = 2
#传参 这里传入视频从那一秒开始，这里需要设置为 0
start = int(sys.argv[2])

# 需要检测标注的时间位置[0,1,2,3,4,5,6,7,8,9,10]
frames = range(start, seconds+1)

# num_frames 存放对应图片的编号
num_frames = []

for i in frames:
    num_frames.append(i*30+1)
#遍历./frames
for filepath,dirnames,filenames in os.walk(r'../Dataset/frames'):
    filenames=sorted(filenames)
    for filename in filenames:
        if str(chooseSecond*30+1) in filename:
            srcfile = filepath + '/' + filename
            dstpath = './chooseVideoFrame/' + filename
            # 复制文件
            shutil.copy(srcfile, dstpath)
            print(filename)
        
