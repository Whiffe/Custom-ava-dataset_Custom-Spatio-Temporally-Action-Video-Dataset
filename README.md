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
## AI platform. AI 平台
The AI platform I use is: [https://cloud.videojj.com/auth/register?inviter=18452&activityChannel=student_invite](https://cloud.videojj.com/auth/register?inviter=18452&activityChannel=student_invite) <br>
我使用的AI平台：[https://cloud.videojj.com/auth/register?inviter=18452&activityChannel=student_invite](https://cloud.videojj.com/auth/register?inviter=18452&activityChannel=student_invite)

The following operations are all done on this platform.<br>
以下的操作均在该平台的基础上完成。

Instance mirroring selection：Pytorch 1.8.0，python 3.8，CUDA 11.1.1 <br>
实例镜像选择：Pytorch 1.8.0，python 3.8，CUDA 11.1.1
![image](https://img-blog.csdnimg.cn/c6544a25f8a748c88ff4451cd1fceb39.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6K6h566X5py66KeG6KeJLeadqOW4hg==,size_20,color_FFFFFF,t_70,g_se,x_16)

## 2.2 project download. AI平台与项目下载
为了让项目可以快速下载，我将项目同步到了码云：[https://gitee.com/YFwinston/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset.git](https://gitee.com/YFwinston/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset.git)
```python
cd /home
git clone https://gitee.com/YFwinston/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset.git

```

# 3 数据集视频准备
The video is 1 randomly selected from the AVA dataset, and I will crop 3 10-second segments from this video:<br>
视频是从AVA数据集中随机选择了1个，我会从这个视频中裁剪出3个10秒的片段：
```python
https://s3.amazonaws.com/ava-dataset/trainval/2DUITARAsWQ.mp4
```
Execute the following code on the AI platform:<br>
在AI平台执行：
```python
cd /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset/videos
wget https://s3.amazonaws.com/ava-dataset/trainval/2DUITARAsWQ.mp4 -O ./1.mp4
```
![image](https://img-blog.csdnimg.cn/1f996811ec164f08b21f04e42220601a.png)
# 4 Video cropping and frame extraction 视频裁剪与抽帧
## 4.1 install ffmpeg 安装ffmpeg
We use ffmpeg for video cropping and frame extraction, so install ffmpeg first<br>
本文使用ffmpeg进行视频裁剪与抽帧，所以先安装ffmpeg
```python
conda install x264 ffmpeg -c conda-forge -y
```
## 4.2 video cropping 视频裁剪
Execute the code under /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset:<br>
在/home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset下执行：

```python
cd /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset
sh cut_video.sh
```
