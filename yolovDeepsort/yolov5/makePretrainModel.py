import torch

# 默认加载
net = torch.load('/user-data/yolov5File/crowdhuman_vbody_yolov5m.pt')
# 用CPU加载
# net = torch.load('model_final.pth',map_location=torch.device('cpu'))

# Net中的key
for k in net.keys():
    print(k)

net_only_model = {"model": net["model"],"optimizer": net["optimizer"],"epoch": net["epoch"]}
torch.save(net_only_model, '../../imageDatasetDetection/pretainModel/crowdhuman_vbody_yolov5m_pretrained.pt')
