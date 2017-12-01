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
            images              (dict): Dictionary object containing information about each of the images 
                                        in the uploaded image set
            current_image       (dict): Dictionary object containing information about the currently selected
                                        base (background) image
            total_num_faces     (int) : Total number of faces present in the uploaded image set
            
    """
    
    def __init__(self): 
        """Initialize the FaceSwap object
        """
        self.images = {}
        self.faces = {}
        self.current_image = {}
        self._current_image_id = None
        self.total_num_faces = -1
        
    def set_image(self, image_id): 
        """Set the current base (background) image. 
        
            Get all necessary information for the background image to have 
            faces replaced. 
            
            Args: 
                image_id (str): String representing the image_id 
                
            Returns: 
                current_image (dict): Dictionary object containing information about 
                                        the selected image
                                        
            Raises: 
                Exception: Image ID is not present
        """
        try: 
            self.current_image = {}
            self.current_image['img_data'] = self.images[image_id]['img_data']
            self.current_image['face_image'] = self.images[image_id]['facial_edge'].face_img
            self.current_image['facial_edge'] = self.images[image_id]['facial_edge']
            self.current_image['faces'] = self.images[image_id]['faces']
            self.current_image['id'] = image_id
            return self.current_image
        except Exception: 
            raise Exception("Image ID %s not present" % image_id)
        
    def reset(self): 
        """Reset the FaceSwap object back to its initial state.
        """
        self.images = {}
        self.faces = {}
        self.current_image = {}
        self._current_image_id = None
        self.total_num_faces = -1
    
    def upload_image(self, image): 
        """Upload a new image to the FaceSwap image set
        
            Creates a new image id entry in the images dictionary
            with a new FacialEdge instance. Faces are detected in the
            image and compared to previously detected faces in other 
            uploaded images (if any have been uploaded). If a face in the
            new image matches a pre-existing face, then the corresponding
            face ID is assigned to the face, otherwise a new face ID is
            created. 
            
            Args: 
                image (array): Image data representing a new image to be added to the 
                                FaceSwap set
                                
            Returns: 
                image ID of newly uploaded image
                
            Raises: 
                Exception: Error uploading new image
        """
        try: 
            new_id = "image_id%s" % len(self.images)
            self.images[new_id] = {}
            self.images[new_id]['img_data'] = image
            # Compute faces in images 
            self.images[new_id]['facial_edge'] = Facial_Edge.Facial_Edge(image)
            self.images[new_id]['facial_edge'].identify()
            self.images[new_id]['faces'] = {}
            print("Found %d faces in image" % len(self.images[new_id]['facial_edge'].face_options))
            # Determine if those faces match previously found faces
            for face in range(0, len(self.images[new_id]['facial_edge'].face_options)): 
                # Select a face from the new image
                self.images[new_id]['facial_edge'].select_face(face)
                max_corr_coef = 0.0
                matching_id = None
                # Iterate through all of the uploaded images looking for the max similarity
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
                        print(curr_corr_coef)
                # Didn't find a good match - this is probably a new face
                if max_corr_coef < .6:
                    self.total_num_faces += 1
                    new_face_id = "face_id%d" % self.total_num_faces
                    self.images[new_id]['faces'][new_face_id] = {}
                    self.images[new_id]['faces'][new_face_id]['location'] = self.images[new_id]['facial_edge'].face_options[face]
                    self.images[new_id]['faces'][new_face_id]['index'] = face
                    (x, y, w, h) = self.images[new_id]['facial_edge'].face_options[face]
                    self.images[new_id]['faces'][new_face_id]['face_data'] = self.images[new_id]['img_data'][y:y+h, x:x+w, :]
                else: 
                    # This face has a match - assign it the faceID of the match
                    self.images[new_id]['faces'][matching_id] = {}
                    self.images[new_id]['faces'][matching_id]['location'] = self.images[new_id]['facial_edge'].face_options[face]
                    self.images[new_id]['faces'][matching_id]['index'] = face
                    (x, y, w, h) = self.images[new_id]['facial_edge'].face_options[face]
                    self.images[new_id]['faces'][matching_id]['face_data'] = self.images[new_id]['img_data'][y:y+h, x:x+w, :]
            return new_id
        
        except Exception: 
            raise Exception("Error uploading new image")
            
    def get_face_dims(self, face_id): 
        """Returns the bounding box for the specified faceid. 
        
            Args: 
                    face_id (str): Face ID corresponding to a face present in the current image
                    
            Returns: 
                The bounding box of the face ID specified from the currently selected image
                
            Raises: 
                Exception: Face ID not present in selected image
                
            Face dimensions are returned as an array
        """
        try: 
            return self.current_image['faces'][face_id]['location']
        except Exception: 
            raise Exception("Face ID %s not present in selected image" % face_id)
        
    def delete_image(self, image_id):
        """Delete an image from the uploaded image set
        
            Deletes an image from the uploaded set. Does nothing
            if the imageID doesn't exist in the dictionary since
            that means it's already gone. 
            
            Args: 
                image_id (str): Image ID to be deleted 
        """
        # Remove dict entry from images dict 
        try: 
            self.images.pop(image_id)
        except KeyError: 
            # image isn't in dict, we're good
            pass
    
    def get_current_image(self): 
        """Returns the image data of the currently selected image. 
        
            Returns: 
                Image data
                
            Raises: 
                Exception: Unable to return image data. Try selecting an image first. 
        
        """
        try: 
            return self.current_image['img_data']
        except Exception: 
            raise Exception("Unable to return image data. Try selecting an image first.")
    
    def process_face(self, image_id, face_id): 
        """ Replace a face in the currently selected image. 
        
            Args: 
                image_id (str): Image ID of the image from which to extract the face 
                face_id  (str): Face ID of the face that should be replaced in the selected image
                
            Returns: 
                The resulting stitched image
                
            Raises: 
                Exception: Error swapping faces.
        """
        # Get information about the face to be swapped
        face_index = self.current_image['faces'][face_id]['index']
        new_face_img_data = self.images[image_id]['img_data']
        new_face_bb = self.images[image_id]["faces"][face_id]['location']

        # Determine face overlap and register
        face = self.current_image['facial_edge'].select_face(face_index).replace_face(new_face_img_data, new_face_bb)
        face_mask = face.mask
        new_face_mask = face.new_face_mask
        print("Detected faces")
        
        # Stitch the images together
        stitch = IStitch.IStitch(np.float64(self.current_image['img_data']), np.float64(new_face_mask), face_mask).stitch_img()
        self.current_image['img_data'] = stitch.stitched_img_
        print("Stiched Images")
        return self.current_image['img_data']
        
        