#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 19:56:36 2017

@author: mrb114
"""

import Facial_Edge
import IReg
import IStitch
import matplotlib.pyplot as plt
import scipy.misc
import numpy as np

# Read in images 
bad_img_path = '/Users/mrb114/Documents/2016-2017/Image Processing/Project/repo/ECE6258/Images/one_face/Elena/Elena_closed.jpg'
good_img_path = '/Users/mrb114/Documents/2016-2017/Image Processing/Project/repo/ECE6258/Images/one_face/Elena/Elena_smile.jpg'
bad_img = np.float64(plt.imread(bad_img_path))
good_img = np.float64(plt.imread(good_img_path))
print("Read in images")

# Register the two images 
reg = IReg.IReg(bad_img, good_img).register()
good_img_reg = reg.float['Image0']['registered']
registered_image_path = '/Users/mrb114/Documents/2016-2017/Image Processing/Project/repo/ECE6258/Images/one_face/Elena/Elena_smile_reg.jpg'
scipy.misc.imsave(registered_image_path, np.uint8(good_img_reg))
print("Registered images")

# Detect faces in images - only one face in image so select it at index 0
face = Facial_Edge.Facial_Edge(bad_img).identify().select_face(0).locate_face(good_img_reg)
face_mask = face.mask
mask_img_path = '/Users/mrb114/Documents/2016-2017/Image Processing/Project/repo/ECE6258/Images/one_face/Elena/Elena_mask.jpg'
scipy.misc.imsave(mask_img_path, np.uint8(face_mask*255))
print("Detected faces")

# Stitch the images together
stitch = IStitch.IStitch(bad_img, good_img_reg, face_mask).stitch_img()
stitched_img_path = '/Users/mrb114/Documents/2016-2017/Image Processing/Project/repo/ECE6258/Images/one_face/Elena/Elena_stitched.jpg'
scipy.misc.imsave(stitched_img_path, stitch.stitched_img_)
print("Stiched Images")

