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
![image](https://img-blog.csdnimg.cn/8e9b191bb72e41ee96b508ad0230a4e5.png)
## 4.3 video frame 视频抽帧
Referring to the ava dataset, crop 30 frames per second <br>
参考ava数据集，每秒裁剪30帧<br>

Execute the code under /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset:<br>
在/home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset 下执行：

```python
cd /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset
bash cut_frames.sh 
```
![image](https://img-blog.csdnimg.cn/ff14789c0a3743e584ea11de15dfc517.png)
![image](https://img-blog.csdnimg.cn/334197c4599e4a12ab594dd8133730a4.png)

## 4.4 Consolidate and downscale frames 整合与缩减帧
The structure of the frames folder generated in Section 4.3 will be inconvenient in the subsequent yolov5 detection, so I put all the pictures in a folder (choose_frames_all) in the following way.<br>
4.3节中产生的frames文件夹的结构，在后续yolov5检测时会出现不方便，所以我采用下面的方式，将所有的图片放在了一个文件夹（choose_frames_all）中。<br>

It should be noted that not all images need to be detected and labeled. In the 10-second video, the detection labels are: x_000001.jpg, x_000031.jpg, x_000061.jpg, x_000091.jpg, x_0000121jpg, x_000151.jpg, x_000181. jpg, x_000211.jpg, x_000241.jpg, x_000271.jpg, x_000301.jpg.<br>
需要注意的是，并不是，所有图片都需要检测与标注，在10秒的视频中，检测标注：x_000001.jpg、x_000031.jpg、x_000061.jpg、x_000091.jpg、x_0000121jpg、x_000151.jpg、x_000181.jpg、x_000211.jpg、x_000241.jpg、x_000271.jpg、x_000301.jpg。<br>

Execute the code under /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset:<br>
在/home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset 下执行：

```python
cd /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset 
python choose_frames_all.py 10 0
```
In the above code, 10 represents the length of the video, and 0 represents the start from the 0th second.<br>
其中10代表视频长度，0代表从第0秒开始 <br>
![image](https://img-blog.csdnimg.cn/8fbb68efa7ac407db1317b1e5d202753.png)

## 4.5 Not consolidate and downscale frames 不整合的缩减帧
The consolidate and downscale frames in 4.4 is for the detection of yolov5, and not consolidate and downscale frames here is for the labeling of VIA.
4.4的整合与缩减是为了yolov5的检测，这里的不整合的缩减是为了VIA的标注。<br>

Execute the code under /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset:<br>
在/home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset 下执行：
```python
cd /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset 
python choose_frames.py 10 0
```
![image](https://img-blog.csdnimg.cn/f5501f08cd7941c692b702f0af25f985.png)
![image](https://img-blog.csdnimg.cn/9041d1ad34ca435ebd67c2f3e1bce3c8.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAQ1Yt5p2o5biG,size_15,color_FFFFFF,t_70,g_se,x_16)

# 5 yolov5 and deep sort installation. yolov5与deep sort 安装

##  5.1 Install 安装
run the following code<br>
运行以下代码：<br>
```
cd /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/yolovDeepsort
pip install -r requirements.txt
pip install opencv-python-headless==4.1.2.30

wget https://github.com/ultralytics/yolov5/releases/download/v6.1/yolov5s.pt -O /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/yolovDeepsort/yolov5/yolov5s.pt 
mkdir -p /root/.config/Ultralytics/
wget  https://ultralytics.com/assets/Arial.ttf -O /root/.config/Ultralytics/Arial.ttf
```
The reason for using deep sort: In preparation for generating [train/val].csv, dense_proposals_[train/val/test].pkl will not use the detection results of deep sort.<br>
采用deep sort的原因：为生成[train/val].csv做准备，dense_proposals_[train/val/test].pkl不会用到deep sort的检测结果。<br>

## 5.2 Detect choose_frames_all 对choose_frames_all进行检测


```python
cd /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/yolovDeepsort
python ./yolov5/detect.py --source ../Dataset/choose_frames_all/ --save-txt --save-conf 
```
The result is stored in: /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/yolovDeepsort/yolov5/runs/detect/exp <br>
结果存储在：/home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/yolovDeepsort/yolov5/runs/detect/exp <br>

![image](https://img-blog.csdnimg.cn/f92b6d91cfb94eb0866ac37704f3d888.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAQ1Yt5p2o5biG,size_20,color_FFFFFF,t_70,g_se,x_16)

# 6 Generate dense_proposals_train.pkl 生成dense_proposals_train.pkl

Execute the code under /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/yolovDeepsort/mywork：
在 /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/yolovDeepsort/mywork下运行：

```python
cd /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/yolovDeepsort/mywork
python dense_proposals_train.py ../yolov5/runs/detect/exp/labels ./dense_proposals_train.pkl show
```

# 7 import via 导入via

## 7.1 choose_frames_all_middle
The choose_frames folder under /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset contains 11 pictures in the 10-second video, but the final generated annotation file does not contain the first 2 pictures and The last 2 pictures. So you need to create a choose_frames_middle folder to store the folders without the first 2 pictures and the last 2 pictures.<br>
/home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset 下的 choose_frames 文件夹中包含10秒视频中11张图片，但是在最后生成的标注文件，不包含前2张图片和后2张图片。所以需要创建一个choose_frames_middle文件夹，存放不含前2张图片与后2张图片的文件夹。<br>

```python
cd /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset/
python choose_frames_middle.py
```
![image](https://img-blog.csdnimg.cn/db8205ef31f0417194a3f40d9bd8caf2.png)

## 7.2 Generate via annotation file 生成via标注文件
自定义动作在：/home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/yolovDeepsort/mywork/dense_proposals_train_to_via.py文件中，具体位置如下图：<br>
The custom action is in: /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/yolovDeepsort/mywork/dense_proposals_train_to_via.py file, the specific location is as follows:<br>
![image](https://img-blog.csdnimg.cn/dc0220d520414c7e82d9fe66eb949e6c.png)

Execute the code under /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/yolovDeepsort/mywork/:<br>
在/home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/yolovDeepsort/mywork/下执行:<br>
```python
cd /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/yolovDeepsort/mywork/
python dense_proposals_train_to_via.py ./dense_proposals_train.pkl ../../Dataset/choose_frames_middle/
```
The generated annotation files are saved in: /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/choose_frames_middle<br>
生成的标注文件保存在：/home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/choose_frames_middle中<br>
![image](https://img-blog.csdnimg.cn/0ad5591962b64fceb90f2a26a7fa98f1.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAQ1Yt5p2o5biG,size_15,color_FFFFFF,t_70,g_se,x_16)
## 7.3 Remove the default value of via 去掉via默认值
标注时有默认值，这个会影响我们的标注，需要取消掉。<br>
There is a default value when labeling, which will affect our labeling and needs to be canceled.<br>

我尝试了很多次，想在生成via标注文件时，去掉标注选项中的默认值，但还是没有实现，那就在生成之后，直接对via的json文件进行操作，去掉默认值。<br>
I have tried many times and want to remove the default value in the annotation option when generating the via annotation file, but it is still not implemented. Then after the generation, directly operate the via json file and remove the default value.<br>

Execute the code under /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/:<br>
在：/home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/下运行<br>

```python
cd /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset
python chang_via_json.py 
```
![image](https://img-blog.csdnimg.cn/de6866f0ef484a3ea909ce5bda598857.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAQ1Yt5p2o5biG,size_15,color_FFFFFF,t_70,g_se,x_16)

## 7.5 Download choose_frames_middle and VIA annotation 下载choose_frames_middle与VIA标注
Compress the choose_frames_middle file<br>
对choose_frames_middle文件压缩<br>

Execute the code under /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset: <br>
在/home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset中执行：<br>

```python
apt-get update
apt-get install zip
apt-get install unzip

cd /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/Dataset
zip -r choose_frames_middle.zip choose_frames_middle
```
Download choose_frames_middle.zip<br>
下载：choose_frames_middle.zip<br>

Then use via to label<br>
然后使用via进行标注<br>

via official website:[https://www.robots.ox.ac.uk/~vgg/software/via/](https://www.robots.ox.ac.uk/~vgg/software/via/)<br>
via官网：[https://www.robots.ox.ac.uk/~vgg/software/via/](https://www.robots.ox.ac.uk/~vgg/software/via/)<br>

via annotation tool download link: [https://www.robots.ox.ac.uk/~vgg/software/via/downloads/via3/via-3.0.11.zip](https://www.robots.ox.ac.uk/~vgg/software/via/downloads/via3/via-3.0.11.zip)<br>
via标注工具下载链接：[https://www.robots.ox.ac.uk/~vgg/software/via/downloads/via3/via-3.0.11.zip](https://www.robots.ox.ac.uk/~vgg/software/via/downloads/via3/via-3.0.11.zip)<br>

Click in the annotation tool: via_image_annotator.html<br>
点击标注工具中的： via_image_annotator.html<br>

![image](https://img-blog.csdnimg.cn/fec0e87d18ab48c2af8299791a1e71af.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAQ1Yt5p2o5biG,size_18,color_FFFFFF,t_70,g_se,x_16)

The following picture is the interface of via, 1 represents adding pictures, 2 represents adding annotation files <br>
下图是via的界面，1代表添加图片，2代表添加标注文件<br>

![image](https://img-blog.csdnimg.cn/6c896dd36f284f2286867510c705a7de.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAQ1Yt5p2o5biG,size_20,color_FFFFFF,t_70,g_se,x_16)

Import the image, open the annotation file (note, open x_proposal_s.json), the final result:<br>
导入图片，打开标注文件（注意，打开x_proposal_s.json），最后结果：<br>
![image](https://img-blog.csdnimg.cn/ba44be0e5d454a2ba063e363b179daea.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAQ1Yt5p2o5biG,size_20,color_FFFFFF,t_70,g_se,x_16)

# 8 Extraction of via annotation information. via标注信息的提取
After action annotation, the annotation information of via is saved as a json file. The json file contains: the name of the video, the number of the video frame, the boundding box of the human, and the number of the action category.<br>
经过动作标注，via的标注信息保存为json文件，json文件中包含：视频的名字、视频帧的编号、人的坐标值、动作类别编号<br>

These information are required for the annotation file, and the information in the json file needs to be integrated. This section is to integrate the information in the via.<br>
这些信息都是标注文件所需要的，需要把json文件中的信息整合，这一节就是对via中信息做整合。<br>

## 7.1 ava_train
The following figure is the ava annotation file (ava_train.csv)<br>
下图是ava标注文件（ava_train.csv）<br>

![image](https://img-blog.csdnimg.cn/0af268f7e8a94fda87dfc75797ee38da.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAQ1Yt5p2o5biG,size_20,color_FFFFFF,t_70,g_se,x_16)
Column 1: The name of the video<br>
第一列：视频的名字<br>

Column 2: the video frame ID, for example, the frame at 15:02 is expressed as 902, and the frame at 15:03 is expressed as 903<br>
第二列：视频帧ID，比如15:02这一帧，表示为902，15:03这一帧表示为903<br>

Column 3-6: the boundding box of the human (x1, y1, x2, y2)<br>
第三列到第六列： 人的坐标值（x1，y1，x2，y2）<br>

Column 7: Action category number<br>
第七列：动作类别编号<br>

Column 8: Person's ID<br>
第八列：人的ID<br>

At present, there is no ID of the last column in our data, and everything else is generated, so let's extract this information first.<nr>
目前，我们的数据中没有最后一列的ID，其它都生成了，所以我们先将这些信息提取出来。<br>
  
## 7.2 Analysis of via Json file. via Json 解析

Parse the json parsing website using the runoob platform: [https://c.runoob.com/front-end/53/](https://c.runoob.com/front-end/53/)
解析使用菜鸟平台的json解析网站：[https://c.runoob.com/front-end/53/](https://c.runoob.com/front-end/53/)



  
  
  
  
  
