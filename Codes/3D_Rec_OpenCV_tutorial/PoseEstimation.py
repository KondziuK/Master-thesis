from os import listdir
import cv2
import numpy as np

im_path_left = r'../Stereovision_ZAW/images_left/'
im_path_right = r'../Stereovision_ZAW/images_right/'
filename_list = [f for f in listdir(im_path_left)]

dist = np.loadtxt('dist.txt')
mtx = np.loadtxt('mtx.txt')

def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img


def draw2(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1,2)

    # draw ground floor in green
    img = cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)

    # draw pillars in blue color
    for i,j in zip(range(4),range(4,8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)

    # draw top layer in red color
    img = cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)

    return img

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
axis2 = np.float32([[0,0,0], [0,3,0], [3,3,0], [3,0,0],
                   [0,0,-3],[0,3,-3],[3,3,-3],[3,0,-3] ])

for fname in filename_list:
    img = cv2.imread(im_path_left + fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

    if ret == True:
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

        # Find the rotation and translation vectors.
        retval, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)

        # project 3D points to image plane
        # imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
        imgpts, jac = cv2.projectPoints(axis2, rvecs, tvecs, mtx, dist)

        # img = draw(img,corners2,imgpts)
        img = draw2(img, corners2, imgpts)
        cv2.imshow('img',img)
        if cv2.waitKey(0) & 0xFF == ord('s'):
            cv2.imwrite(fname[:6]+'.png', img)

cv2.destroyAllWindows()




