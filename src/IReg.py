#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Image Registration.
"""
import numpy as np
import cv2

class IReg():
    """Image Registration class. 
    
        A class to be used for registering 1 or more images to a 
        single image. 
        
        Attributes: 
            ref: A reference image to which all floating images will be registered to
            float: A image or set of images which will be registered to the reference image stored
                    in the following dictionary format: 
                    self.float: {
                            'Image0': {
                                    'original': [input data for floating image 0],
                                    'registered': [registered data for floating image 0]
                            },
                            
                            ...
                            
                            'ImageN': {
                                    'original': [input data for floating image N]
                                    'registered': [registered data for floating image N]
                            }
                    }
            
    """

    def __init__(self, reference_image, float_image=None):
        """Initializes an image registration class object. 
        
            Args: 
                reference_image (ndarray): a reference image to be used for registration 
                float_image     (ndarray): Optional input. A floating image to register to the 
                                            reference image. 
                                            
            Returns: 
                IReg object
        """
        self.ref = reference_image
        self.float = {}
        self._num_floats = 0
        if float_image is not None:
            self.float['Image0'] = {}
            self.float['Image0']['original'] = float_image
            self.float['Image0']['registered'] = None
            self._num_floats += 1
        
    def add_floating_img(self, img): 
        """Adds a floating image to the images to be registered
        
            Args: 
                img (ndarray): An additional image to register to the reference image
                
            Returns: 
                IReg object
        """
        self._num_floats += 1
        self.float['Image%d' % self._num_floats] = {}
        self.float['Image%d' % self._num_floats]['original'] = img
        self.float['Image%d' % self._num_floats]['registered'] = None      
        return self
                  
    def register(self):
        """Registers the reference image to the floating image(s).
           
           Uses DFT image registration from imreg_dft package on each channel
           of the reference and float image(s). Registration parameters are
           averaged across channels and average is applied to each channel 
           to produce the registered final image. The resulting registered image 
           is stored in the object float member variable following the prescribed
           format: 
               
           object.float: {
                   'Image 0': {
                           'original': [original image data]
                           'registered': [registered image data]
                   }
           }
           
           Returns: 
               IReg object
        """
        # For each float image
        for float_image in np.arange(0, self._num_floats): 
            if self.float['Image%d' % float_image]['registered'] is not None: 
                continue
            print('processing float image %d' % float_image)
            curr_float = self.float['Image%d' % float_image]['original']

            im1_gray = cv2.cvtColor(self.ref,cv2.COLOR_BGR2GRAY)
            im2_gray = cv2.cvtColor(curr_float,cv2.COLOR_BGR2GRAY)
            
            # Find size of image1
            sz = self.ref.shape
             
            # Define the motion model
            #warp_mode = cv2.MOTION_TRANSLATION
            warp_mode = cv2.MOTION_HOMOGRAPHY
             
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
                registered_img = cv2.warpPerspective (curr_float, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
            else :
                # Use warpAffine for Translation, Euclidean and Affine
                registered_img = cv2.warpAffine(curr_float, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);
            self.float['Image%d' % float_image]['registered'] = registered_img
        return self
    