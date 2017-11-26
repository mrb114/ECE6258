#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Image stitching based off of input images and a mask
"""
import cv2
import numpy as np

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
      
    def stitch_img(self): 
        """Stitch the images together. 
        """        
        # Need to pad with zeros to make the dimensions powers of 2 
        img1 = self._pad_img(self.img1_)
        img2 = self._pad_img(self.img2_)
        mask = self._pad_img(self.mask_)
        
        # Define number of levels in pyramid 
        num_levels = 6
           
        # Apply gaussian pyramids
        gaussian_img1 = self._gaussian_pyramid(img1, num_levels)
        gaussian_img2 = self._gaussian_pyramid(img2, num_levels)
        gaussian_mask = self._gaussian_pyramid(mask, num_levels)
        
        # Apply laplacian pyramids
        laplacian_img1 = self._laplacian_pyramid(gaussian_img1, num_levels)
        laplacian_img2 = self._laplacian_pyramid(gaussian_img2, num_levels)
        
        # Apply mask and reconstruct
        self.stitched_img_ = self._reconstruct_pyramid(laplacian_img1, laplacian_img2, gaussian_mask, num_levels)
        self.stitched_img_ = self.stitched_img_[0:np.shape(self.img1_)[0], 0:np.shape(self.img1_)[1], :]
        return self
        
    def _next_power_two(number):
        # Returns next power of 2 of a number
        return np.ceil(np.log2(number))
        
    def _pad_img(self, img): 
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
        
    def _gaussian_pyramid(self, img, n): 
        pyramid = [img]
        for i in np.arange(0, n): 
            img= cv2.pyrDown(img)
            pyramid.append(img)
        return pyramid
        
    def _laplacian_pyramid(self, gaussian_pyramid, n): 
        n -= 1
        pyramid = [gaussian_pyramid[n]]
        for i in np.arange(n, 0, -1): 
            pyramid.append(gaussian_pyramid[i - 1]-cv2.pyrUp(gaussian_pyramid[i]))
        return pyramid 
        
    def _reconstruct_pyramid(self, lap_img1, lap_img2, gaus_mask, n): 
        lap_summed = []
        count = n - 1
        for lap1,lap2 in zip(lap_img1, lap_img2):
            gm = gaus_mask[count]
            lap_summed.append(lap2*gm + lap1*(1. - gm))
            count -= 1
        recon = lap_summed[0]
        for i in np.arange(1,6):
            recon = cv2.pyrUp(recon)+ lap_summed[i]
        return np.uint8(recon)
 