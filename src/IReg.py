#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Image Registration.
"""
import numpy as np
import imreg_dft as ird

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
            print('processing float image 1')
            curr_float = self.float['Image%d' % float_image]['original']
            registration_vector = np.zeros([1,2])
            scale = 0; 
            angle = 0; 
            # Compute registration for each channel 
            for channel in np.arange(0, np.shape(self.ref)[2]): 
                print('processing channel %d' % channel)
                result = ird.similarity(self.ref[:,:,channel], curr_float[:, :, channel], numiter=3)
                registration_vector += result['tvec']
                scale += result['scale']
                angle += result['angle']
            # Average registration vector for each channel 
            registration_vector /= np.shape(self.ref)[2]
            scale /= np.shape(self.ref)[2]
            angle /= np.shape(self.ref)[2]
            # Apply average registration vector to entire image 
            registered_img = np.zeros(np.shape(self.ref))
            for channel in np.arange(0, np.shape(self.ref)[2]): 
                print('applying transformation to channel %d' % channel)
                registered_img[:, :, channel] = ird.transform_img(curr_float[:, :, channel], scale=scale, angle=angle, tvec=registration_vector[0])
            self.float['Image%d' % float_image]['registered'] = registered_img
        return self
    