# Hardsub2SRT

Tested on Linux with WSL2

Requirements are opencv for C++ (Install it with your package manager).
Compile `threshold.cc` with the following command
```
g++ -O3 -std=c++11 threshold.cc `pkg-config --cflags --libs opencv4` -o ocr
```

Python requirements are easyocr, jellyfish, srt

I'll probably convert the bash script to python and also may convert threshold to python but I'm worried about the performance hit.
Had to use easyOCR instead of tesseract cause tesseract was just not as accurate.

Here's the link to the tesseract code if you can fix it. https://pastebin.com/7ja1NQeP. I assume it would be more performant.
