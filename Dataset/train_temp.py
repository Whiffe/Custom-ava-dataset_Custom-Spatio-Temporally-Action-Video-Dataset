import csv
 
train_personID_path = './train_personID.csv'
train_without_personID_path = './train_without_personID.csv'

train_personID = []
train_without_personID = []

with open(train_personID_path) as csvfile:
    csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
    for row in csv_reader:           
        train_personID.append(row)

with open(train_without_personID_path) as csvfile:
    csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
    for row in csv_reader:          
        train_without_personID.append(row)

dicts = []
for data in train_without_personID:
    isFind = False
    for temp_data in train_personID:
        # 属于同一个视频
        if int(data[0]) == int(temp_data[0]):
            # 属于同一张图片
            if int(data[1]) == int(temp_data[1]):
                if abs(float(data[2])-float(temp_data[2]))<0.005 and abs(float(data[3])-float(temp_data[3]))<0.005 and abs(float(data[4])-float(temp_data[4]))<0.005 and abs(float(data[5])-float(temp_data[5]))<0.005:
                    # temp_data[6]-1 代表将ID-1，原因是ID从0开始计数
                    dict = [data[0],data[1],data[2],data[3],data[4],data[5],data[6],int(temp_data[6])-1]
                    dicts.append(dict)
                    isFind = True
                    break
    if not isFind:
        dict = [data[0],data[1],data[2],data[3],data[4],data[5],data[6],-1]
        dicts.append(dict)

with open('./train_temp.csv',"w") as csvfile: 
    writer = csv.writer(csvfile)
    writer.writerows(dicts)