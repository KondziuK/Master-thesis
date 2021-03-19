import cv2
import numpy as np
import matplotlib.pyplot as plt

left_img = cv2.imread('../../../../../Downloads/zaw_1_12/lab_5_ZAW/aloes/aloeL.jpg')
right_img = cv2.imread('../../../../../Downloads/zaw_1_12/lab_5_ZAW/aloes/aloeR.jpg')

stereo_bm = cv2.StereoBM_create(32)
dispmap_bm = stereo_bm.compute(cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY),
                               cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY))

stereo_sgbm = cv2.StereoSGBM_create(0, 32)
dispmap_sgbm = stereo_sgbm.compute(left_img, right_img)

plt.figure(figsize=(12,10))
plt.subplot(221)
plt.title('left')
plt.imshow(left_img[:,:,[2,1,0]])
plt.subplot(222)
plt.title('right')
plt.imshow(right_img[:,:,[2,1,0]])
plt.subplot(223)
plt.title('BM')
plt.imshow(dispmap_bm, cmap='gray')
plt.subplot(224)
plt.title('SGBM')
plt.imshow(dispmap_sgbm, cmap='gray')
plt.show()

# # !/usr/bin/env python
# # Python 2/3 compatibility
# from __future__ import print_function
# import sys
# import numpy as np
# import cv2
#
# print('load and downscale images')
# imgL = cv2.pyrDown(cv2.imread('../data/aloeL.jpg'))
# imgR = cv2.pyrDown(cv2.imread('../data/aloeR.jpg'))
#
# min_disp = 16
# if sys.argv[1] > 0:
#     min_disp = int(sys.argv[1])
# num_disp = 112 - min_disp
# window_size = 17
#
# stereo = cv2.StereoBM_create(numDisparities=num_disp, blockSize=window_size)
# stereo.setMinDisparity(min_disp)
# stereo.setNumDisparities(num_disp)
# stereo.setBlockSize(window_size)
# stereo.setDisp12MaxDiff(0)
# stereo.setUniquenessRatio(10)
# stereo.setSpeckleRange(32)
# stereo.setSpeckleWindowSize(100)
#
# print('compute disparity')
# grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
# grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
# disp = stereo.compute(grayL, grayR).astype(np.float32) / 16.0
# disp_map = (disp - min_disp) / num_disp
#
# print('display')
# cv2.imshow('left', imgL)
# cv2.imshow('disparity', disp_map)
# cv2.waitKey()
# cv2.destroyAllWindows()

