from os import listdir
import cv2
import numpy as np
import matplotlib.pyplot as plt

def drawlines(img1,img2,lines,pts1,pts2):
    ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
    r,c = img1.shape
    img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR)
    for r,pt1,pt2 in zip(lines,pts1,pts2):
        color = tuple(np.random.randint(0,255,3).tolist())
        x0,y0 = map(int, [0, -r[2]/r[1] ])
        x1,y1 = map(int, [c, -(r[2]+r[0]*c)/r[1] ])
        img1 = cv2.line(img1, (x0,y0), (x1,y1), color,1)
        img1 = cv2.circle(img1,tuple(pt1),5,color,-1)
        img2 = cv2.circle(img2,tuple(pt2),5,color,-1)
    return img1,img2

def calibrate(img, mtx, dist):

    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    # by using cv2.undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    return dst




im_path_left = r'../Stereovision_ZAW/images_left/'
im_path_right = r'../Stereovision_ZAW/images_right/'
filename_list = [f for f in listdir(im_path_left)]

dist = np.loadtxt('dist.txt')
mtx = np.loadtxt('mtx.txt')


img1 = cv2.imread(im_path_left+'left01.jpg',0)  #queryimage # left image
img1 = calibrate(img1, mtx, dist)

img2 = cv2.imread(im_path_right+'right01.jpg',0) #trainimage # right image
img2 = calibrate(img2, mtx, dist)

# Initiate STAR detector
orb = cv2.ORB_create()

# find the keypoints with ORB
kp1 = orb.detect(img1, None)
kp2 = orb.detect(img2, None)

# compute descriptors with orb
kp1, des1 = orb.compute(img1, kp1)
kp2, des2 = orb.compute(img2, kp2)

### Brute force matching with ORB Descriptors

# Create BFMatcher object
bf = cv2.BFMatcher()

# Match desciptors
matches = bf.knnMatch(des1, des2, k=2)

# Sort them in the order of their distance.
# Apply ratio test



good = []
pts1 = []
pts2 = []
for m, n in matches:
    if m.distance < 0.9 * n.distance:
        good.append([m])
        pts2.append(kp2[m.trainIdx].pt)
        pts1.append(kp1[m.queryIdx].pt)

pts1 = np.int32(pts1)
pts2 = np.int32(pts2)
F, mask = cv2.findFundamentalMat(pts1,pts2,cv2.FM_LMEDS)

# We select only inlier points
pts1 = pts1[mask.ravel()==1]
pts2 = pts2[mask.ravel()==1]




# Find epilines corresponding to points in right image (second image) and
# drawing its lines on left image
lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1,1,2), 2,F)
lines1 = lines1.reshape(-1,3)
img5,img6 = drawlines(img1,img2,lines1,pts1,pts2)

# Find epilines corresponding to points in left image (first image) and
# drawing its lines on right image
lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1,1,2), 1,F)
lines2 = lines2.reshape(-1,3)
img3,img4 = drawlines(img2,img1,lines2,pts2,pts1)

plt.subplot(121),plt.imshow(img5)
plt.subplot(122),plt.imshow(img3)
plt.show()