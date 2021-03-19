import cv2
import numpy as np
import matplotlib.pyplot as plt

img_l = cv2.imread('../../../../../Downloads/zaw_1_12/lab_5_ZAW/aloes/aloeL.jpg')
img_r = cv2.imread('../../../../../Downloads/zaw_1_12/lab_5_ZAW/aloes/aloeR.jpg')

gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
gray_r = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)

L = np.float32(gray_l)
R = np.float32(gray_r)

W2 = 7 #pol dlugosci bloku
dX = W2
dY = 0

YY, XX = gray_l.shape[:2] #height, width

u = np.zeros((YY, XX))
v = np.zeros((YY, XX))

for j in range(W2+1, YY-W2-1):
    for i in range(W2+dX+1, XX-dX-W2-1):
        IO = np.float32(L[j - W2:j + W2 + 1, i - W2:i + W2 + 1])
        min_dist = 1000000
        for j_1 in range(j):
            j_1 = j
            for i_1 in range(i - dX, i + dX + 1):
                JO = np.float32(R[j_1 - W2:j_1 + W2 + 1, i_1 - W2:i_1 + W2 + 1])
                dist = np.sum((cv2.absdiff(JO, IO)))
                if (dist < min_dist):
                    min_dist = dist
        print(min_dist)

