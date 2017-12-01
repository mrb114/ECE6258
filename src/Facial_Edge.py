#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Facial Edge Detection
"""

import cv2
import numpy as np
import os
import IReg


class Facial_Edge():
    """Facial edge detection class
    
    Utilizes the face_recognition package to identify and segment faces and 
    facial features from images. 
    
    Attributes: 
        img             (ndarray): An image from which faces are identified
        face_options    (list)   : A list of indices representing the indices of the faces in the image
        selected_face   (ndarray)  : An image representing the face selected
        
    """
    def __init__(self, image):
        """Initialize Facial Edge Object
        
            Args: 
                image (ndarray): Input image
        """
        self.img = np.uint8(image)
        self.face_options = []
        self.selected_face = -1
        self._rot90 = False
        cascade_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascade_frontalface_alt.xml')
        profile_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascade_profileface.xml')
        self.face_cascade = cv2.CascadeClassifier(cascade_filepath)
        self.profile_cascade = cv2.CascadeClassifier(profile_filepath)
        
    def identify(self, img=None): 
        """Identify faces in image
        """
        return_indices = True
        if img is None: 
            img = self.img.copy()
            return_indices = False
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_options = self.face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)
        face_options2 = self.profile_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)
        combo_face_options = []
        mask = np.zeros(np.shape(img))

        for (x, y, w, h) in face_options2:
            combo_face_options.append([x, y, w, h])
            mask[x:x+w, y:y+h] = 1
             
        for (x, y, w, h) in face_options:
            if np.sum(mask[x:x+w, y:y+h])/(w*h) < .1:
                combo_face_options.append([x, y, w, h]) 
        if return_indices: 
            return combo_face_options
        self.face_img = img.copy()
        for (x, y, w, h) in combo_face_options:
            cv2.rectangle(self.face_img, (x, y), (x+w, y+h), (0, 255, 0), 4)
        self.face_options = combo_face_options
        if len(self.face_options) == 0: 
            raise Exception("Error: Unable to detect faces in images")
        return self
        
    def select_face(self, index): 
        """Identify a face as the key face to be replaced
        
            The provided index will indicate which face to select as the "key" face
            for replacement in the image. The identify function should be executed
            prior to the execution of this function. 
            
            Args: 
                index (int): The index of the face to be chosen from the list of 
                             coordinates generated in the identify step.
        
        """
        if index > len(self.face_options): 
            raise ValueError('Error: the index selected exceeds the dimensions available for facial selection.')
        
        x, y, w, h = self.face_options[index]
        self.selected_face = self.img[y:y+h, x:x+w]
        self.selected_face_loc = self.face_options[index]
        return self
        
    def replace_face(self, new_img, new_face_bb): 
        """Replace a known face location in a new image 
        """
        # Initialize mask 
        mask = np.zeros(np.shape(self.img))
        new_face_mask = np.zeros(np.shape(self.img))
        
        # Compare bounding boxes of selected face and new face
        (xS, yS, wS, hS) = self.selected_face_loc
        x, y, w, h = new_face_bb
        w = np.min([w, wS])
        h = np.min([h, hS])
        offset = 30
        selected_face = self.img[yS-offset:yS+h+offset, xS-offset:xS+w+offset, :]
        new_face = new_img[y-offset:y+h+offset, x-offset:x+h+offset, :]
        reg = IReg.IReg(selected_face, new_face).register()
        new_face_reg = reg.float['Image0']['registered']
        mask[yS:yS+h, xS:xS+w] = 1
        new_face_mask[yS-offset:yS+h+offset, xS-offset:xS+w+offset] = np.uint8(new_face_reg)
        indices = new_face_mask <= 0
        new_face_mask[indices] = self.img[indices]
        
        self.mask = mask
        self.new_face_mask = new_face_mask
        return self

    def locate_face(self, new_img): 
        """Identify the selected face in a new image. 
        
            Args: 
                image (filepath): Filepath from which to read input image
                
            Returns: 
                mask (ndarray): A binary mask representing the location of the face in the new image
        """
        # Identify faces in new image
        new_face_options = self.identify(new_img)
        
        # Initialize mask 
        mask = np.zeros(np.shape(self.img))
        new_face_mask = np.zeros(np.shape(self.img))
        
        # Compare each of the selected faces to the face encoding generated from the select_face() function 
        (xS, yS, wS, hS) = self.selected_face_loc
        for i in np.arange(0, len(new_face_options)): 
            if self.compare_faces(self.selected_face_loc, new_face_options[i], self.img, new_img): 
                x, y, w, h = new_face_options[i]
                w = np.min([w, wS])
                h = np.min([h, hS])
                offset = 30
                selected_face = self.img[yS-offset:yS+h+offset, xS-offset:xS+w+offset, :]
                new_face = new_img[y-offset:y+h+offset, x-offset:x+h+offset, :]
                reg = IReg.IReg(selected_face, new_face).register()
                new_face_reg = reg.float['Image0']['registered']
                mask[yS:yS+h, xS:xS+w] = 1
                new_face_mask[yS-offset:yS+h+offset, xS-offset:xS+w+offset] = np.uint8(new_face_reg)
                indices = new_face_mask <= 0
                new_face_mask[indices] = self.img[indices]
                break
        self.mask = mask
        self.new_face_mask = new_face_mask
        return self
    
    def compare_faces(self, face1, face2, img1, img2): 
        (x1, y1, w1, h1) = face1
        (x2, y2, w2, h2) = face2
        w = np.max([w1, w2])
        h = np.max([h1, h2])
        if x1+w > img1.shape[1] or x2+w > img2.shape[1]: 
            w = np.min([w1, w2])
        if y1+h > img1.shape[0] or y2+h > img2.shape[0]: 
            h = np.min([h1, h2])
        face1_img = img1[y1:y1+h, x1:x1+w, :]
        face2_img = img2[y2:y2+h, x2:x2+w, :]
        corr_mat = np.corrcoef(face1_img.flat, face2_img.flat)
        corr_coef = corr_mat[0, 1]
        #print(corr_coef)
        return corr_coef
        """if corr_coef > .7:
            return True
        return False"""
