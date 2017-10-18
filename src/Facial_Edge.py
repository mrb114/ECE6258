#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Facial Edge Detection
"""

import face_recognition
import os


class Facial_Edge():
    """Facial edge detection class
    
    Utilizes the face_recognition package to identify and segment faces and 
    facial features from images. 
    
    Attributes: 
        img             (ndarray): An image from which faces are identified
        face_options    (list)   : A list of indices representing the indices of the faces in the image
        selected_face   (ndarray)  : An image representing the face selected
        
    """
    def __init__(self, image_loc):
        """Initialize Facial Edge Object
        
            Args: 
                image_loc (filepath): Filepath from which to read input image
        """
        self.img = face_recognition.load_image_file(os.path.abspath(image_loc))
        self.face_options = []
        self.selected_face = -1
        
    def identify(self): 
        """Identify faces in image
        """
        self.face_options = face_recognition.face_locations(self.img, model="cnn")
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
        
        top, right, bottom, left = self.face_options[index]
        self.selected_face = self.img[top:bottom, left:right]
        self._face_encoding = face_recognition.face_encodings(self.selected_face)[0]

    def locate_face(self, image_loc): 
        """Identify the selected face in a new image. 
        
            Args: 
                image_loc (filepath): Filepath from which to read input image
                
            Returns: 
                mask (ndarray): A binary mask representing the location of the face in the new image
        """
        # Identify faces in new image
        # Compare each of the selected faces to the face encoding generated from the select_face() function 
        # Once identified, apply a mask to the selected face - we may need to apply some facial segmentation on the sub region
        # Return the mask indicating where the face is in the image
        pass
    