#! /bin/bash

########################### constants ###########################
input=xiaowangzi.mkv # input video file
wcrop=2 
hcrop=5
Stime=00:01:31 # how long is the op
Rtime=00:22:21 # when does the ed start
fps=1 # how many frames should ffmpeg capture per second
lang=ch_sim # language code found here 'https://www.jaided.ai/easyocr'
accuracy=0.7 # the code finds the jaro distance between two sentences to see how similar they are cause ocr messes up often. this value is how similar should the sentences be to be considered the same
shift='00:01:30.667' # this is basically just to line up the subs. Its not working that well rn though

## NO SLASH AT THE END!!
framedir=img_new # folder to hold the frame captures
thresholdir=wimg_new # folder to hold the thresholded frames
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

