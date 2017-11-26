#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Image stitching based off of input images and a mask
"""
import numpy as np
import Facial_Edge
import IReg
import IStitch

class FaceSwap(): 
    """Face swap object for swapping faces
    
        Attributes: 
            
    """
    
    def __init__(self): 
        self.images = {}
        self.faces = {}
        self.current_image = None
        self._current_image_id = None
        self.face_swap = None
        self.img_reg = None
        self.total_num_faces = 0
        
    def set_image(self, image_id): 
        self.current_image = self.images.get(image_id).get('image')
        self._current_image_id = image_id
        return self.images.get(image_id).get('faces')
    
    def upload_image(self, image): 
        new_id = "image_id%s" % len(self.images)
        self.images[new_id] = {}
        self.images[new_id]['img_data'] = image
        # Add image as reference image if first or floating image otherwise
        if self.img_reg is None: 
            self.img_reg = IReg.IReg(image)
        else: 
            # we already have a reference image, add a new floating image
            self.img_reg.add_floating_img(image)
            # register the floating image
            self.img_reg.register()
        print("Registered image")
        # Compute faces in images 
        self.images[new_id]['facial_edge'] = Facial_Edge.Facial_Edge(image)
        self.images[new_id]['facial_edge'].identify()
        self.images[new_id]['faces'] = {}
        print("Found %d faces in image" % len(self.images[new_id]['facial_edge'].face_options))
        # Determine if those faces are in the faces dict
        for face in range(0, len(self.images[new_id]['facial_edge'].face_options)): 
            print('Working on face %d' % face)
            self.images[new_id]['facial_edge'].select_face(face)
            face_found = False
            for image_id in range(0, len(self.images)): 
                curr_id = "image_id%s" % image_id
                if curr_id == new_id: 
                    continue
                for curr_face in self.images[curr_id]['faces'].keys():
                    if curr_face in self.images[new_id]['faces'].keys(): 
                        break
                    curr_encoding = self.images[curr_id]['faces'][curr_face]['encoding']
                    if self.images[new_id]['facial_edge'].compare_faces(curr_encoding): 
                        self.images[new_id]['faces'][curr_face] = {}
                        self.images[new_id]['faces'][curr_face]['encoding'] = self.images[new_id]['facial_edge']._face_encoding 
                        self.images[new_id]['faces'][curr_face]['location'] = self.images[new_id]['facial_edge'].face_options[face]
                        break
            if not face_found:
                self.total_num_faces += 1
                new_face_id = "face_id%d" % self.total_num_faces
                self.images[new_id]['faces'][new_face_id] = {}
                self.images[new_id]['faces'][new_face_id]['encoding'] = self.images[new_id]['facial_edge']._face_encoding 
                self.images[new_id]['faces'][new_face_id]['location'] = self.images[new_id]['facial_edge'].face_options[face]
                
        # Match pre-existing faces from dict to those in image
        # If faces aren't in dict, then add them 
        # Record faceids in image dict 
        
    def get_face_dims(self, face_id): 
        return self.images[self.current_image_id]['faces'][face_id]
        
    
    def delete_image(self, image_id):
        # Remove dict entry from images dict 
        try: 
            self.images.pop(image_id)
        except KeyError: 
            # image isn't in dict, we're good
            pass
    
    def get_current_image(self): 
        return self.current_image
    
    def process_face(self, face_id): 
        pass
        """
        images = {
                "imageid1": {
                        "img_data": np.array(image_data),
                        "faces": {
                                "faceid1": {
                                        "location": [x, y, xDim, yDim], 
                                        "encoding": encoding_val
                                        }
                                "faceid2":{
                                        "location": [x, y, xDim, yDim], 
                                        "encoding": encoding_val
                                        }
                                }
                        },
                "imageid2": {
                        "img_data": np.array(image_data),
                        "faces": {
                                "faceid1": {
                                        "location": [x, y, xDim, yDim], 
                                        "encoding": encoding_val
                                        } 
                                "faceid2": {
                                        "location": [x, y, xDim, yDim], 
                                        "encoding": encoding_val
                                        }
                                }
                        }
                }
        faces = {
                "faceid1": {
                        'imageid1': 0, 
                        'imageid2': 1
                        }
                "faceid2": {
                        'imageid2': 0
                        }
        }
                        """
        