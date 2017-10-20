#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Image stitching based off of input images and a mask
"""
#import cv2
import numpy as np
import math
import os
import matplotlib.pyplot as plt
import scipy
import sys
from scipy.signal import convolve2d
from scipy.stats import norm

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
  
    def stitch_img(self): 
        """Stitch the images together. 
        """
        # The line directly below this doesn't actually work too poorly but could be improved on
        #self.stitched_img_ = np.uint8(self.mask_*self.img2_ + np.logical_not(self.mask_)*self.img1_)
        
        # Need to pad with zeros to make the dimensions powers of 2 
        img1 = _pad_img(self.img1_)
        img2 = _pad_img(self.img2_)
        mask = _pad_img(self.mask_)
        
        # Define number of levels in pyramid 
        num_levels = 6
        
           
        # Apply gaussian pyramids
        gaussian_img1 = _gaussian_pyramid(img1, num_levels)
        gaussian_img2 = _gaussian_pyramid(img2, num_levels)
        gaussian_mask = _gaussian_pyramid(mask, num_levels)
        
        # Apply laplacian pyramids
        laplacian_img1 = _laplacian_pyramid(gaussian_img1, num_levels)
        laplacian_img2 = _laplacian_pyramid(gaussian_img2, num_levels)
        laplacian_mask = _laplacian_pyramid(gaussian_mask, num_levels)
        
        # Apply mask and reconstruct
        self.stitched_img_ = _reconstruct_pyramid(laplacian_img1, laplacian_img2, laplacian_mask)
        self.stitched_img = self.stitched_img[0:np.shape(self.img1)[0], 0:np.shape(self.img1)[1]]
        return self
    def _next_power_two(number):
        # Returns next power of 2 of a number - what to zero pad to
        return np.ceil(np.log2(number))
    def _pad_img(img): 
        # pad image here to closest power of 2 in x and y dimensions 
        length = np.shape(img)[0]
        width = np.shape(img)[1]
        # Check if the dimension are powers of 2
        next_power_length = np.ceil(np.log2(length))
        next_power_width = np.ceil(np.log2(width))
        deficit_length =int(2**next_power_length - length);
        deficit_width = int(2**next_power_width - width);

        imagenew = np.pad(img, ((0, deficit_length), (0, deficit_width), (0,0)), 'constant') 
        return imagenew
        
    def _gaussian_pyramid(img, n): 
        pyramid = [img]
        for i in np.arange(0, n): 
            pyramid.append(cv2.pyrDown(img))
        return pyramid
        
    def _laplacian_pyramid(gaussian_pyramid, n): 
        n -= 1
        pyramid = [gaussian_pyramid[n]]
        for i in np.arange(n, 0, -1): 
            pyramid.append(cv2.subtract(gaussian_pyramid[i - 1], cv2.pyrUp(gaussian_pyramid[i])))
        return pyramid 
        
    def _reconstruct_pyramid(img1, img2, mask): 
        lap_summed = []
        for lap1,lap2, lapMask in zip(img1,img2, mask):
            lap_summed.append(np.hstack((lap1*lapMask, lap2*np.logical_not(lapMask))))
        lap_recon = lap_summed[0]
        for i in np.arange(1,6):
            lap_recon = cv2.add(cv2.pyrUp(lap_recon), lap_summed[i])

 