#IN_DATA_DIR="../Dataset/videos"
#OUT_DATA_DIR="../Dataset/video_crop"
#TXT_DIR="./cutVideo.txt"
#bash cutVideo.sh ../Dataset/videos ../Dataset/video_crop ./cutVideo.txt

#IN_DATA_DIR输入视频的路径
IN_DATA_DIR=$1
#OUT_DATA_DIR输出视频的路径
OUT_DATA_DIR=$2
#TXT_DIR进行视频裁剪的信息（包含输入视频名，每个视频裁剪的时间起始节点）
TXT_DIR=$3

#判断OUT_DATA_DIR这个路径存在么，不存在就创建
if [[ ! -d "${OUT_DATA_DIR}" ]]; then
  echo "${OUT_DATA_DIR} doesn't exist. Creating it.";
  mkdir -p ${OUT_DATA_DIR}
fi

#c是用来辅助将TXT_DIR中的信息存放到accounts数组中
c=0
for line in `cat ${TXT_DIR}`
do
  account=$line
  accounts[$c]=$account
  ((c++))
done

#循环accounts数组，读出其中的数据
for e in ${accounts[@]}
do
  #在循环数组时，判断当前循环的元素包含 . 么，如果包含 . ,就代表着时视频名，而非起始点
  #如果是视频名，就取出扩展名，如mp4，avi等，然后在取出没有扩展名的视频名，如10001.mp4取出变成10001
  #c2是计数，计数该视频会裁剪出多少个视频
  if [[ $e == *.* ]]
  then
    video=${IN_DATA_DIR}/${e}
    ext=${e##*.}
    videoname=${e%.*}
    c2=0
  else
    #start代表裁剪的起始点
    start=${e}
    ((c2++))
    #c2，c3的作用是，让裁剪视频名是占2位即01、02、03...
    if [[ ${#c2} < 2 ]]
    then
      c3=0${c2}
    else
      c3=${c2}
    fi
    #输出视频名由3部分构成
    #前2位数（10～99）代表视频大类，中间3位数（001～999）代表该大类视频下收集的各个视频，最后2位数（01～99）代表某一视频裁剪的编号。
    out_name="${OUT_DATA_DIR}/${videoname}${c3}.${ext}"
    ffmpeg -i "${video}" -ss ${start} -t 15 "${out_name}"
fi
done
