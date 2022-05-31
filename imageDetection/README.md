
imageDetection这个文件夹作用在于制作课堂学生检测数据集，包含：视频裁剪、视频抽帧、视频帧的选择、选择帧的检测、对检测进行微调、对微调的标签重训练。

原始视频是存放在：'../Dataset/videos/' 文件夹下面<br>
裁剪的视频存放在：'../Dataset/video_crop' 文件夹下面<br>
视频抽帧存放在： ''<br>
# 1 各个文件的作用
## via3_tool.py
via3_tool.py是via官方文档，来自：[JN-OpenLib-mmaction2](https://github.com/Wenhai-Zhu/JN-OpenLib-mmaction2)

## yolo2via.py
yolo2via.py的作用是将yolov5的检测标签转化为via所能识别的格式
