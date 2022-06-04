
imageDetection这个文件夹作用在于制作课堂学生检测数据集，包含：视频裁剪、视频抽帧、视频帧的选择、选择帧的检测、对检测进行微调、对微调的标签重训练。

原始视频是存放在：'../Dataset/videos/' 文件夹下面<br>
视频取名：10001，前2位数（10～99）代表视频大类，后3位数（001～999）代表该大类视频下收集的各个视频。<br><br>
裁剪的视频存放在：'../Dataset/video_crop' 文件夹下面<br>
裁剪的视频取名：1000101，前2位数（10～99）代表视频大类，中间3位数（001～999）代表该大类视频下收集的各个视频，最后2位数（01～99）代表某一视频裁剪的编号。<br><br>
视频抽帧存放在： '../Dataset/frames'<br>
<br>


# 1 各个文件的作用
## via3_tool.py
via3_tool.py是via官方文档，来自：[JN-OpenLib-mmaction2](https://github.com/Wenhai-Zhu/JN-OpenLib-mmaction2)

## yolo2via.py
yolo2via.py的作用是将yolov5的检测标签转化为via所能识别的格式

## cutVideos.sh
cutVideos.sh的作用是将videos文件夹下的视频按照cutVideos.txt的内容裁剪位多个15秒的视频，并将裁剪的视频放在video_crop文件夹下。
## cutVideos.txt
cutVideos.txt中存储了视频名及视频裁剪的起始点，如：10002.mp4 1340 2165 2710 2746，代表视频10002.mp4从第1340秒、第2165秒、第2710秒、第2746秒开始裁剪，裁剪长度为15秒，裁剪长度为15秒。

## cut_frames.sh
cut_frames.sh的作用是将每一个裁剪的视频抽帧，然后以每一个视频对应一个文件夹，该文件夹存放该视频抽帧图片。

## chooseVideoFrame.py
chooseVideoFrame.py的作用是从每一个视频帧文件夹中选择一张（默认中间的一张），作为课堂学生目标检测的数据集。

## yolo2via.py
yolo2via.py的作用是将yoloV5的检测结果转化为via可以识别使用的格式
