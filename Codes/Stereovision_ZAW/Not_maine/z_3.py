import cv2
import numpy as np
import matplotlib.pyplot as plt
#from sklearn.metrics import mean_squared_error

img_l = cv2.imread('../../../../../Downloads/zaw_1_12/lab_5_ZAW/aloes/aloeL.jpg')
img_r = cv2.imread('../../../../../Downloads/zaw_1_12/lab_5_ZAW/aloes/aloeR.jpg')

g_l = cv2.imread('../../../../../Downloads/zaw_1_12/lab_5_ZAW/aloes/groundL.png')
g_r = cv2.imread('../../../../../Downloads/zaw_1_12/lab_5_ZAW/aloes/groundR.png')

gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
gray_r = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)


min_disp = 16
num_disp = 96
window_size = 17

block_matching = cv2.StereoBM_create(numDisparities=num_disp, blockSize=window_size)

block_matching.setMinDisparity(min_disp)
block_matching.setDisp12MaxDiff(0)
block_matching.setUniquenessRatio(10)
block_matching.setSpeckleRange(32)
block_matching.setSpeckleWindowSize(100)

disparity_bm = block_matching.compute(gray_l, gray_r).astype(np.float32) #/ 16.0
disp_map_bm = (disparity_bm / np.max(disparity_bm)) * 255


sgm = cv2.StereoSGBM_create(minDisparity=min_disp, numDisparities=num_disp, blockSize=window_size, disp12MaxDiff=0, uniquenessRatio=10, speckleWindowSize=100, speckleRange=32)
disparity_sgm = sgm.compute(gray_l, gray_r)#.astype(np.float32) / 16.0
disp_map_sgm = (disparity_sgm / np.max(disparity_sgm)) * 255

plt.figure(figsize=(11, 9))
plt.subplot(221)
plt.title('Block matching')
plt.imshow(disp_map_bm, cmap='gray')
plt.subplot(222)
plt.title('Semi-Global Matching')
plt.imshow(disparity_sgm, cmap='gray')
plt.subplot(223)
plt.title('Groudtruth_L')
plt.imshow(g_l)
plt.subplot(224)
plt.title('Oryginalny_L')
plt.imshow(img_l[:, :, [2, 1, 0]])
plt.show()

# Mozna porównac metode z mapa np. wskaznikiem 'bad2.0' (procent pikseli o błedzie dysparycji wiekszym niz dwa) lub 'rms' (root mean square).

dim = disparity_bm.shape[0]*disparity_bm.shape[1]
g_l_1 = g_l[:, :, 1]

#rms_bm = mean_squared_error(g_l_1, disparity_bm)
rms_bm = np.sqrt(np.sum(np.power(disp_map_bm - g_l_1, 2)) / dim)
print('Wskaznik rms dla metody Block matching wynosi:', rms_bm)


# rmse_bm = np.linalg.norm(disparity_bm - g_l_1) / np.sqrt(dim)
# print(rmse_bm)
#
# rms2_bm = np.sqrt(np.mean((disparity_bm - g_l_1)**2))
# print(rms2_bm)


rms_sgm = np.sqrt(np.sum(np.power(disp_map_sgm - g_l_1, 2)) / dim)
print('Wskaznik rms dla metody Semi-Global Matching wynosi:', rms_sgm)

