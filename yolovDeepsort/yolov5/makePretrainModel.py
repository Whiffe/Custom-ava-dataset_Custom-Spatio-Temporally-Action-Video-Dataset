import torch
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--weight_dir', default='/user-data/yolov5File/crowdhuman_vbody_yolov5m.pt',type=str, help="the path of crowdhuman_vbody_yolov5m.pt")
parser.add_argument('--preWeight_dir', default='../../imageDetection/pretainModel/crowdhuman_vbody_yolov5m_pretrained.pt',type=str, help="the path of crowdhuman_vbody_yolov5m_pretrained.pt")

arg = parser.parse_args()

# 默认加载
net = torch.load(arg.weight_dir)
# 用CPU加载
# net = torch.load('model_final.pth',map_location=torch.device('cpu'))

# Net中的key
for k in net.keys():
    print(k)

net_only_model = {"model": net["model"],"optimizer": net["optimizer"],"epoch": net["epoch"]}
torch.save(net_only_model, arg.preWeight_dir)
