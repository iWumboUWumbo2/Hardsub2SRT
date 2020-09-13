#! /bin/bash

########################### constants ###########################
input=xiaowangzi.mkv
wcrop=2
hcrop=5
Stime=00:01:31
Rtime=00:22:21
fps=24
lang=ch_sim
accuracy=0.7
shift='00:01:30.667'

## NO SLASH AT THE END!!
framedir=img_new
thresholdir=wimg_new
##################################################################

mkdir -p $framedir
mkdir -p $thresholdir

timediff=$(( $(date -d "$Rtime" "+%s") - $(date -d "$Stime" "+%s") ))
Etime=$(printf ""%02d:%02d:%02d"\n" $(($timediff/3600)) $(($timediff%3600/60)) $(($timediff%60)))

ffmpeg -ss $shift -i $input -to $Etime -vf "crop=in_w/$wcrop:in_h/$hcrop:in_w*(1-1/$wcrop)/2:in_h, fps=$fps" $framedir/%09d.png

mkdir -p $thresholdir

for file in $framedir/*
do 
    name=${file##*/}
    echo $name
    ./threshold $framedir/$name $thresholdir/$name
done

python3 ocr.py -d $thresholdir -l $lang -a $accuracy -fps $fps -ss $shift -o "${input%%.*}.srt"
# python3 ocr.py -d $framedir -l $lang -a $accuracy -fps $fps -ss $shift -o "${input%%.*}.srt"

