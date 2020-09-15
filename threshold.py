import sys
import cv2
import numpy as np

def main():
    inputFile, outputFile = (sys.argv[1], sys.argv[2])
    im = cv2.imread(inputFile)
    cv2.Scalar(200, 200, 200)
    wim = cv2.inRange(im, np.array([200, 200, 200]), np.array([255, 255, 255]))
    cv2.imwrite(filename=outputFile, img=wim)

if __name__ == "__main__":
    main()
