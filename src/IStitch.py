#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Image stitching based off of input images and a mask
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

class IStitch(): 
    """Image stitching class. 
    
        Uses two input images along with a mask identifying an area of the second image
        to stich into the first.
        
        Attributes: 
            img1_           (ndarray): Base image onto which the stitching will take place 
            img2_           (ndarray): Secondary image from which the masked data will be taken
            mask_           (ndarray): Identifies area of images to stitch together
            stitched_img_   (ndarray): Stitched image
    """

    def __init__(self, img1, img2, mask): 
        """Write about this fxn
        
            Args: 
                
        """
        self.img1_ = img1
        self.img2_ = img2 
        self.mask_ = mask 
        img_file = 'ECE6258/Images/one_face/Elena/Elena_closed.jpg'
        img2_file = 'ECE6258/Images/one_face/Elena/Elena_smile.jpg'
        temp_img1 = plt.imread(img_file)
        self._test_mask = np.zeros(np.shape(temp_img1))
        top = 741
        bottom = 1891
        left = 1508
        right = 357
        self._test_mask[top:bottom, left:right] = 1
        
        # Include error check here if the three volumes are not the same size 
        if "not the same size": 
            raise Exception("error msg here")
            
    def stitch_img(): 
        """Stitch the images together. 
        """
        self.stitched_img_ = self.mask_*self.img2_ + np.logical_not(self.mask_)*self.img1_
        return self