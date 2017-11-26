#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 19:56:36 2017

@author: mrb114
"""

import cv2
import Facial_Edge
import IReg
import IStitch
import matplotlib.pyplot as plt
import scipy.misc
import numpy as np
import os

# Read in images 
#bad_img_path = '/Users/mrb114/Documents/2016-2017/Image Processing/Project/repo/ECE6258/Images/one_face/Elena/Elena_closed.jpg'
#good_img_path = '/Users/mrb114/Documents/2016-2017/Image Processing/Project/repo/ECE6258/Images/one_face/Elena/Elena_smile.jpg'
bad_img_path = '/Users/mrb114/Documents/2016-2017/Image Processing/Project/repo/ECE6258/Images/Summer/20150628_115935.jpg'
good_img_path = '/Users/mrb114/Documents/2016-2017/Image Processing/Project/repo/ECE6258/Images/Summer/20150628_115934.jpg'
bad_img = plt.imread(bad_img_path)
good_img = plt.imread(good_img_path)
#bad_img = cv2.imread(bad_img_path)
#good_img = cv2.imread(good_img_path)
bad_img = np.rot90(bad_img, 3)
good_img = np.rot90(good_img, 3)
print("Read in images")

## Register the two images 
#reg = IReg.IReg(bad_img, good_img).register()
#good_img_reg = reg.float['Image0']['registered']
#registered_image_path = '/Users/mrb114/Documents/2016-2017/Image Processing/Project/repo/ECE6258/Images/one_face/Elena/Elena_smile_reg.jpg'
#scipy.misc.imsave(registered_image_path, np.uint8(good_img_reg))
#print("Registered images")

# Detect faces in images - only one face in image so select it at index 0
face = Facial_Edge.Facial_Edge(bad_img).identify().select_face(0).locate_face(good_img)
face = face.select_face(0).locate_face(good_img)
face_mask = face.mask
new_face_mask = face.new_face_mask
mask_img_path = '/Users/mrb114/Documents/2016-2017/Image Processing/Project/repo/ECE6258/Images/one_face/Elena/Elena_mask.jpg'
scipy.misc.imsave(mask_img_path, np.uint8(face_mask*255))
print("Detected faces")

# Stitch the images together
stitch = IStitch.IStitch(np.float64(bad_img), new_face_mask, face_mask).stitch_img()
stitched_img_path = '/Users/mrb114/Documents/2016-2017/Image Processing/Project/repo/ECE6258/Images/one_face/Elena/Elena_stitched.jpg'
scipy.misc.imsave(stitched_img_path, stitch.stitched_img_)
print("Stiched Images")



# Instead of registering images to one another try registering just the faces to one another


#fpath = '../Images/Parents_Farther/20161218_162922_resized.jpg'
#fpath = '../Images/Parents_Farther/20161218_162920_resized.jpg'
#fpath = '../Images/Parents_Farther/20161218_162930_resized.jpg'
#fpath = '../Images/Summer/20150628_115934.jpg'
fpath = '../Images/Priya/20151024_135925.jpg'
img = cv2.imread(fpath)
img = np.rot90(img,3)
#plt.imshow(img)
min_face = int(np.max(img.shape)/30)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
face_cascade2 = cv2.CascadeClassifier('haarcascade_profileface.xml')
face_options = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)
face_options2 = (face_cascade2.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5))
combo_face_options = []
mask = np.zeros(np.shape(img))
for (x, y, w, h) in face_options:
    combo_face_options.append([x, y, w, h])
    mask[x:x+w, y:y+h] = 1
for (x, y, w, h) in face_options2:
    area = w*h
    avg = np.sum(mask[x:x+w, y:y+h])/area
    if avg < .75:
        combo_face_options.append([x, y, w, h])       
face_img = img.copy()
for (x, y, w, h) in combo_face_options:
    cv2.rectangle(face_img, (x, y), (x+w, y+h), (0, 255, 0), 4)
print(len(combo_face_options))
R = face_img[:,:,2].copy()
B = face_img[:,:,0].copy()
face_img[:,:,2] = B
face_img[:,:,0] = R
os.remove('/Users/mrb114/Documents/2016-2017/Image Processing/Project/repo/ECE6258/src/test_img.jpg')
scipy.misc.imsave('/Users/mrb114/Documents/2016-2017/Image Processing/Project/repo/ECE6258/src/test_img.jpg', face_img)



# Read the images to be aligned
im1 = cv2.imread('/Users/mrb114/Documents/2016-2017/Image Processing/Project/repo/ECE6258/Images/Summer/20150628_115935.jpg')
im2 = cv2.imread('/Users/mrb114/Documents/2016-2017/Image Processing/Project/repo/ECE6258/Images/Summer/20150628_115934.jpg')

# Convert images to grayscale
im1_gray = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
im2_gray = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
 
# Find size of image1
sz = im1.shape
 
# Define the motion model
warp_mode = cv2.MOTION_TRANSLATION
 
# Define 2x3 or 3x3 matrices and initialize the matrix to identity
if warp_mode == cv2.MOTION_HOMOGRAPHY :
    warp_matrix = np.eye(3, 3, dtype=np.float32)
else :
    warp_matrix = np.eye(2, 3, dtype=np.float32)
 
# Specify the number of iterations.
number_of_iterations = 5000;
 
# Specify the threshold of the increment
# in the correlation coefficient between two iterations
termination_eps = 1e-10;
 
# Define termination criteria
criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)
 
# Run the ECC algorithm. The results are stored in warp_matrix.
(cc, warp_matrix) = cv2.findTransformECC (im1_gray,im2_gray,warp_matrix, warp_mode, criteria)
 
if warp_mode == cv2.MOTION_HOMOGRAPHY :
    # Use warpPerspective for Homography 
    im2_aligned = cv2.warpPerspective (im2, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
else :
    # Use warpAffine for Translation, Euclidean and Affine
    im2_aligned = cv2.warpAffine(im2, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);
 
# Show final results
cv2.imshow("Image 1", im1)
cv2.imshow("Image 2", im2)
cv2.imshow("Aligned Image 2", im2_aligned)