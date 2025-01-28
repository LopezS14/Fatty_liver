
import cv2
import numpy as np
 
filenames = 'data/Azul R2.JPG'
img = cv2.imread(filenames)
cv2.imshow('orginal',img)
#sobelprocessing
imgx = cv2.Sobel(img,cv2.CV_16S,1,0,ksize=3)
imgy = cv2.Sobel(img,cv2.CV_16S,0,1,ksize=3)
 #   uint8
imgx_uint8 = cv2.convertScaleAbs(imgx)
imgy_uint8 = cv2.convertScaleAbs(imgy)
 # x, combinación de dirección y
img = cv2.addWeighted(imgx_uint8,0.5,imgy_uint8,0.5,0)
 
cv2.imshow('sobelimg',img)
cv2.waitKey(0)
