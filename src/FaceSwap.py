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
        self.current_image = {}
        self._current_image_id = None
        self.face_swap = None
        self.img_reg = None
        self.total_num_faces = -1
        
    def set_image(self, image_id): 
        self.current_image = {}
        self.current_image['img_data'] = self.images[image_id]['img_data']
        self.current_image['face_image'] = self.images[image_id]['facial_edge'].face_img
        self.current_image['facial_edge'] = self.images[image_id]['facial_edge']
        self.current_image['faces'] = self.images[image_id]['faces']
        self.current_image['id'] = image_id
        return self.current_image
        
    def reset(self): 
        self.images = {}
        self.faces = {}
        self.current_image = {}
        self._current_image_id = None
        self.face_swap = None
        self.img_reg = None
        self.total_num_faces = -1
    
    def upload_image(self, image): 
        new_id = "image_id%s" % len(self.images)
        self.images[new_id] = {}
        self.images[new_id]['img_data'] = image
        # Compute faces in images 
        self.images[new_id]['facial_edge'] = Facial_Edge.Facial_Edge(image)
        self.images[new_id]['facial_edge'].identify()
        self.images[new_id]['faces'] = {}
        print("Found %d faces in image" % len(self.images[new_id]['facial_edge'].face_options))
        # Determine if those faces are in the faces dict
        for face in range(0, len(self.images[new_id]['facial_edge'].face_options)): 
            print('Working on face %d' % face)
            self.images[new_id]['facial_edge'].select_face(face)
            max_corr_coef = 0.0
            matching_id = None
            for image_id in range(0, len(self.images)): 
                curr_id = "image_id%s" % image_id
                
                if curr_id == new_id: 
                    continue
                for curr_face in self.images[curr_id]['faces'].keys():
                    if curr_face in self.images[new_id]['faces'].keys(): 
                        continue
                    curr_corr_coef = self.images[new_id]['facial_edge'].compare_faces(self.images[new_id]['facial_edge'].face_options[face], 
                                                                        self.images[curr_id]['faces'][curr_face]['location'], 
                                                                        self.images[new_id]['img_data'], 
                                                                        self.images[curr_id]['img_data'])
                    if curr_corr_coef > max_corr_coef: 
                        max_corr_coef = curr_corr_coef
                        matching_id = curr_face
            if max_corr_coef < .7:
                self.total_num_faces += 1
                new_face_id = "face_id%d" % self.total_num_faces
                self.images[new_id]['faces'][new_face_id] = {}
                self.images[new_id]['faces'][new_face_id]['location'] = self.images[new_id]['facial_edge'].face_options[face]
                self.images[new_id]['faces'][new_face_id]['index'] = face
                (x, y, w, h) = self.images[new_id]['facial_edge'].face_options[face]
                self.images[new_id]['faces'][new_face_id]['face_data'] = self.images[new_id]['img_data'][y:y+h, x:x+w, :]
            else: 
                self.images[new_id]['faces'][matching_id] = {}
                self.images[new_id]['faces'][matching_id]['location'] = self.images[new_id]['facial_edge'].face_options[face]
                self.images[new_id]['faces'][matching_id]['index'] = face
                (x, y, w, h) = self.images[new_id]['facial_edge'].face_options[face]
                self.images[new_id]['faces'][matching_id]['face_data'] = self.images[new_id]['img_data'][y:y+h, x:x+w, :]
        return new_id
        
    def get_face_dims(self, face_id): 
        return self.current_image['faces'][face_id]['location']
        
    def delete_image(self, image_id):
        # Remove dict entry from images dict 
        try: 
            self.images.pop(image_id)
        except KeyError: 
            # image isn't in dict, we're good
            pass
    
    def get_current_image(self): 
        return self.current_image['img_data']
    
    def process_face(self, image_id, face_id): 
        face_index = self.current_image['faces'][face_id]['index']
        new_face_img_data = self.images[image_id]['img_data']
        new_face_bb = self.images[image_id]["faces"][face_id]['location']

        # Determine face overlap and register
        #face = self.current_image['facial_edge'].select_face(face_index).locate_face(new_face_img_data)
        face = self.current_image['facial_edge'].select_face(face_index).replace_face(new_face_img_data, new_face_bb)
        face_mask = face.mask
        new_face_mask = face.new_face_mask
        print("Detected faces")
        
        # Stitch the images together
        stitch = IStitch.IStitch(np.float64(self.current_image['img_data']), np.float64(new_face_mask), face_mask).stitch_img()
        self.current_image['img_data'] = stitch.stitched_img_
        print("Stiched Images")
        return self.current_image['img_data']
        
        
        """
        images = {
                "imageid1": {
                        "img_data": np.array(image_data),
                        "faces": {
                                "faceid1": {
                                        "location": [x, y, xDim, yDim]
                                        }
                                "faceid2":{
                                        "location": [x, y, xDim, yDim]
                                        }
                                }
                        },
                "imageid2": {
                        "img_data": np.array(image_data),
                        "faces": {
                                "faceid1": {
                                        "location": [x, y, xDim, yDim]
                                        } 
                                "faceid2": {
                                        "location": [x, y, xDim, yDim]
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
        