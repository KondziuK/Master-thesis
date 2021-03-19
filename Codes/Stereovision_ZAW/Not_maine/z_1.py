import cv2
import numpy as np
import matplotlib.pyplot as plt

# kryternia przetwania obliczen (blad+liczba iteracji)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# przygotowanie punktow 2D w postaci: (0,0,0), (1,0,0), (2,0,0) ....,(6,7,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
# tablice do przechowywania punktow obiektow (3D) i punktow na obrazie (2D) dla wszystkich obrazow
objpoints = [] # punkty 3d w przestrzeni (rzeczywsite)
imgpoints = [] # punkty 2d w plaszczyznie obrazu.

for i in range(1, 13):
    # wczytanie obrazu
    img = cv2.imread('images_left/left%02d.jpg' % i)
    # konwersja do odcieni szarosci
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # wyszukiwanie naroznikow na planszy
    ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)
    # jesli znaleniono na obrazie punkty
    if ret == True:
        #dolaczenie wspolrzednych 3D
        objpoints.append(objp)
        # poprawa lokalizacji punktow (podpiskelowo)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        # dolaczenie poprawionych punktow
        imgpoints.append(corners2)
        # wizualizacja wykrytych naroznikow
        cv2.drawChessboardCorners(img, (7, 6), corners2, ret)
        cv2.imshow("Corners", img)
        cv2.waitKey(5)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
#print('Ret:', ret, '\nMTX:', mtx, '\nDist:', dist, '\nRvecs:', rvecs, '\nTvecs:', tvecs)

h, w = img.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0.5, (w,h))

dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

# mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
# dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv2.imwrite('../../../../../Downloads/zaw_1_12/lab_5_ZAW/calibresult.png', dst)
