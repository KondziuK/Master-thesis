import numpy as np
import cv2
from matplotlib import pyplot as plt


im_path_left = r'../Stereovision_ZAW/images_left/'
im_path_right = r'../Stereovision_ZAW/images_right/'
imgL = cv2.imread(im_path_left+'left01.jpg')
imgR = cv2.imread(im_path_right+'right01.jpg')

imgL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
imgR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

# imgL = cv2.imread('tsukuba_l.png',0)
# imgR = cv2.imread('tsukuba_r.png',0)

stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity,'gray')
plt.title('Disparity map')
cv2.imwrite('DisparityMap.png',disparity)
plt.show()