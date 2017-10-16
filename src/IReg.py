#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Image Registration.
"""
import numpy as np

class IReg():
    """Image Registration class. 
    
        A class to be used for registering 1 or more images to a 
        single image. 
        
        Attributes: 
            ref: A reference image to which all floating images will be registered to
            float: A image or set of images which will be registered to the reference image
            
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
            self.float['Image0'] = float_image
            self._num_floats += 1
        return self
        
    def add_floating_img(self, img): 
        """Adds a floating image to the images to be registered
        
            Args: 
                img (ndarray): An additional image to register to the reference image
                
            Returns: 
                IReg object
        """
        self._num_floats += 1
        self.float['Image%d' % self._num_floats] = img
        return self
                  
    def register(self):
        """Registers the reference image to the floating image(s).
        
           Returns: 
               IReg object
        """
        returns self
        
        
    