import cv2
import numpy as np
import matplotlib.pyplot as plt

im_path_left = r'../Stereovision_ZAW/images_left/'
im_path_right = r'../Stereovision_ZAW/images_right/'

# kryternia przerwania obliczen (blad+liczba iteracji)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# przygotowanie punktow 2D w postaci: (0,0,0), (1,0,0), (2,0,0) ....,(6,7,0)
objp = np.zeros((6*7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)
# tablice do przechowywania punktow obiektow (3D) i punktow na obrazie (2D) dla wszystkich obrazow
objpoints = [] # punkty 3d w przestrzeni (rzeczywsite)
imgpoints_l = [] # punkty 2d w plaszczyznie obrazu.
imgpoints_r = [] # punkty 2d w plaszczyznie obrazu.

for i in range(1, 13):
    # wczytanie obrazu
    img_l = cv2.imread(im_path_left+'left%02d.jpg' % i)
    img_r = cv2.imread(im_path_right+'right%02d.jpg' % i)
    # konwersja do odcieni szarosci
    gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
    gray_r = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)
    # wyszukiwanie naroznikow na planszy
    ret_l, corners_l = cv2.findChessboardCorners(gray_l, (7, 6), None)
    ret_r, corners_r = cv2.findChessboardCorners(gray_r, (7, 6), None)
    # jesli znaleniono na obrazie punkty
    if ret_l == True and ret_r == True:
        #dolaczenie wspolrzednych 3D
        objpoints.append(objp)
        # poprawa lokalizacji punktow (podpiskelowo) + dolaczenie poprawionych punktow + wizualizacja wykrytych naroznikow
        corners2 = cv2.cornerSubPix(gray_l, corners_l, (11, 11), (-1, -1), criteria)
        imgpoints_l.append(corners2)
        # #wizualizacja
        # cv2.drawChessboardCorners(img_l, (7, 6), corners2, ret_l)
        # cv2.imshow("Corners", img_l)
        # cv2.waitKey()

        corners2 = cv2.cornerSubPix(gray_r, corners_r, (11, 11), (-1, -1), criteria)
        imgpoints_r.append(corners2)
        # #wizualizacja
        # cv2.drawChessboardCorners(img_r, (7, 6), corners2, ret_r)
        # cv2.imshow("Corners", img_r)
        # cv2.waitKey()


ret_l, mtx_l, dist_l, rvecs_l, tvecs_l = cv2.calibrateCamera(objpoints, imgpoints_l, gray_l.shape[::-1], None, None)
ret_r, mtx_r, dist_r, rvecs_r, tvecs_r = cv2.calibrateCamera(objpoints, imgpoints_r, gray_r.shape[::-1], None, None)
#print('Ret:', ret, '\nMTX:', mtx, '\nDist:', dist, '\nRvecs:', rvecs, '\nTvecs:', tvecs)

retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(objpoints, imgpoints_l, imgpoints_r, mtx_l, dist_l, mtx_r, dist_r, gray_l.shape[::-1])

R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, gray_r.shape[::-1], R, T)

map1_L, map2_L = cv2.initUndistortRectifyMap(cameraMatrix1, distCoeffs1, R1, P1, gray_l.shape[::-1], cv2.CV_16SC2)
map1_R, map2_R = cv2.initUndistortRectifyMap(cameraMatrix2, distCoeffs2, R2, P2, gray_l.shape[::-1], cv2.CV_16SC2)



img_l = cv2.imread(im_path_left+'left01.jpg')
img_r = cv2.imread(im_path_right+'right01.jpg')


dst_L = cv2.remap(img_l, map1_L, map2_L, cv2.INTER_LINEAR) #tutaj jest xle img_l
dst_R = cv2.remap(img_r, map1_R, map2_R, cv2.INTER_LINEAR)

dst_L = cv2.cvtColor(dst_L, cv2.COLOR_BGR2GRAY)
dst_R = cv2.cvtColor(dst_R, cv2.COLOR_BGR2GRAY)


focal_length_r = mtx_r[0][0]
focal_length_l = mtx_l[0][0]
Baseline = T[0]

stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)


disparity = stereo.compute(dst_L, dst_R)

rows, cols = disparity.shape

for i in range(0, rows):
    for j in range(0, cols):
        if disparity[i][j] == 0:
            disparity[i][j] += 1


if 0.0 in disparity:
    print("WTF")

cv2.imshow('ImageL',dst_L)
cv2.imshow('ImageR',dst_R)

plt.imshow(disparity,'gray')
plt.title('Disparity map')


depth_map = (Baseline * focal_length_l)/disparity
depth_map = depth_map/np.amax(depth_map) *255

cv2.imshow('test',depth_map)

plt.show()
cv2.waitKey(0)





