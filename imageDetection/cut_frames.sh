#IN_DATA_DIR="../Dataset/video_crop"
#OUT_DATA_DIR="../Dataset/frames"
#bash cutVideo.sh ../Dataset/video_crop ../Dataset/frames

#IN_DATA_DIR输入裁剪视频的路径
IN_DATA_DIR=$1
#OUT_DATA_DIR输出抽帧的路径
OUT_DATA_DIR=$2

if [[ ! -d "${OUT_DATA_DIR}" ]]; then
  echo "${OUT_DATA_DIR} doesn't exist. Creating it.";
  mkdir -p ${OUT_DATA_DIR}
fi

for video in $(ls -A1 -U ${IN_DATA_DIR}/*)
do
  video_name=${video##*/}

  echo $video_name
  array=(${video_name//./ })
  video_name=${array[0]}
  echo $video_name
  
  out_video_dir=${OUT_DATA_DIR}/${video_name}/
  mkdir -p "${out_video_dir}"

  out_name="${out_video_dir}/${video_name}_%06d.jpg"

  ffmpeg -i "${video}" -r 30 -q:v 1 "${out_name}"
done
