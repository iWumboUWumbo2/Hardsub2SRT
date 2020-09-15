import os
import sys
import easyocr
import unicodedata
import jellyfish as jf
import srt
from datetime import timedelta
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--wimg-dir', dest='wimgdir', type=str, default='wimg', metavar='<dir>', help="Specify location of threshold image directory")
parser.add_argument('-l', '--lang', dest='language', type=str, default='ch_sim', metavar='<lang>', help="Specify language of hardcoded subtitle text")
parser.add_argument('-a', '--accuracy', dest='accuracy', type=float, default=0.7, metavar='<acc>', help="Specify accuracy delta of comparisons between two subtitles")
parser.add_argument('-fps', '--fps', dest='fps', type=int, default=1, metavar='<fps>', help="Specify how many image frames were taken per second")
parser.add_argument('-ss', '--time-shift', dest='timeshift', type=str, default=0, metavar='<timeshift>', help="Specify how far forward the subtitles should be shifted forward in milliseconds")
parser.add_argument('-o', '--output-file', dest='output', type=str, default='xiaowanzi.srt', metavar='<file>', help="Specify filename of srt file")

args = parser.parse_args()

wimg_dir = args.wimgdir + '/'
lang = args.language
accuracy = args.accuracy
fps = args.fps
timeshift = args.timeshift
output_filename= args.output

reader = easyocr.Reader([lang])

def get_filename(fn) -> str:
    basename: str = os.path.basename(fn)
    withoutExt: tuple = os.path.splitext(basename)
    return withoutExt[0]

def txt_cleanup(txt):
    chinese_text = []
    for c in txt:
        if unicodedata.category(c) == 'Lo':
            chinese_text.append(c)
    chinese_text = ''.join(chinese_text)
    
    return chinese_text

frames = []
output_text = []

for f in os.listdir(wimg_dir):
    result = reader.readtext(wimg_dir+f, detail=0)

    frame = get_filename(f)
    text = ''.join(result)

    print(frame + '\t' + text)

    if text:
        frames.append(int(frame))
        output_text.append(txt_cleanup(text))

print('\n\n\n')

for i in range(len(frames)):
    print(str(frames[i]) + '\t' + output_text[i])

subinfo = []

i = 0
while i < len(frames):
    ogframe = frames[i]
    ogTxt = output_text[i]
    while (i < len(frames) and jf.jaro_distance(output_text[i], ogTxt) > accuracy):
        i += 1
    
    if (i < len(frames)):
        edframe = frames[i-1]+1
    subinfo.append([ogframe, edframe, ogTxt])

print('\n\n\n')
print(subinfo)

def timeshift_to_ms(ts):
    stime = ts.split('.')
    ms = stime[-1]
    h, m, s = stime[0].split(':')

    return (int(h) * 3600 + int(m) * 60 + int(s)) * 1000 + int(ms)

def get_time_in_ms(frameno):
    ms = frameno / fps * 1000
    delta = timedelta(milliseconds=(ms+timeshift_to_ms(timeshift)))
    return delta

subs = []
index = 1
for info in subinfo:
    stime, etime, text = info
    sub = srt.Subtitle(index=index, start=get_time_in_ms(stime), end=get_time_in_ms(etime), content=text)
    subs.append(sub)
    index += 1

subtext = srt.compose(subs)

with open(output_filename, 'w') as file:
    file.write(subtext)

print(f'\nSubtitle outputted to {output_filename}')