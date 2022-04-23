# Custom ava dataset, Custom Spatio Temporally Action Video Dataset
Custom ava dataset, Multi-Person Video Dataset Annotation Method of Spatio-Temporally Actions <br>
自定义ava数据集，多人视频的时空动作数据集标注方法 <br>

ava dataset paper: [https://arxiv.org/pdf/1705.08421.pdf](https://arxiv.org/pdf/1705.08421.pdf) <br>
ava数据集论文：[https://arxiv.org/pdf/1705.08421.pdf](https://arxiv.org/pdf/1705.08421.pdf) <br>

下面是我在CSDN、知乎、B站的同步内容：<br>
CSDN：<br>
知乎：<br>
B站：<br>

# 1 Dataset‘s folder structure 数据集文件结构

![image](https://github.com/Whiffe/Custom-ava-dataset_Multi-Person-Video-Dataset-Annotation-Method-of-Spatio-Temporally-Actions/blob/95307633663fa3103a46de75220aabf1174013ca/images/DatasetFolderStructure.png)

# 2 AI platform and project download.  AI平台与项目下载
The AI platform I use is: [https://cloud.videojj.com/auth/register?inviter=18452&activityChannel=student_invite](https://cloud.videojj.com/auth/register?inviter=18452&activityChannel=student_invite) <br>
我使用的AI平台：[https://cloud.videojj.com/auth/register?inviter=18452&activityChannel=student_invite](https://cloud.videojj.com/auth/register?inviter=18452&activityChannel=student_invite)

The following operations are all done on this platform.<br>
以下的操作均在该平台的基础上完成。

Instance mirroring selection：Pytorch 1.8.0，python 3.8，CUDA 11.1.1 <br>
实例镜像选择：Pytorch 1.8.0，python 3.8，CUDA 11.1.1
![image](https://img-blog.csdnimg.cn/c6544a25f8a748c88ff4451cd1fceb39.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6K6h566X5py66KeG6KeJLeadqOW4hg==,size_20,color_FFFFFF,t_70,g_se,x_16)

# 3 数据集视频准备
视频是从AVA数据集中随机选择了3个：
```python
https://s3.amazonaws.com/ava-dataset/trainval/2DUITARAsWQ.mp4
```
将视频下载到极链AI平台的镜像实例，代码如下：
 （如果速度慢了，可以现采用迅雷下载，然后上传）

```python

wget https://s3.amazonaws.com/ava-dataset/trainval/1ReZIMmD_8E.mp4 -O /home/Dataset/videos/1.mp4
wget https://s3.amazonaws.com/ava-dataset/trainval/_ithRWANKB0.mp4 -O /home/Dataset/videos/2.mp4
wget https://s3.amazonaws.com/ava-dataset/trainval/2DUITARAsWQ.mp4 -O /home/Dataset/videos/3.mp4
```
