# 1 The role of some self-made files 部分自制文件的作用
## 1.1 makePretrainModel.py
makePretrainModel.py文件的作用是自制预训练模型<br>
在制作课堂学生数据集的过程中，我采用经过crowdedhuman数据集训练后的权重，但是这个权重并不能直接用，需要将该模型制作为预训练模型(我是这样认为的)。<br>
采用yolov5在crowdedhuman下预训练模型的好处在于，可以使用较少的数据量，训练出较好的效果。<br>
制作预训练模型的代码，我参考：制作自己的Detectron2预训练模型：[https://zhuanlan.zhihu.com/p/147336249](https://zhuanlan.zhihu.com/p/147336249)<br>

