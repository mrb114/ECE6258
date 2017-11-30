#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()

from gevent import wsgi
import FaceSwap
import os
import json
import matplotlib.pyplot as plt
import scipy.misc
import numpy as np

from flask_cors import CORS
from flask import Flask, jsonify, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),'static')
ALLOWED_EXTENSIONS = set([ 'bmp', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
fs_obj = FaceSwap.FaceSwap()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=['POST'])
def upload_img():
    try:
        files = request.files['file']
    except Exception: 
        return json.dumps({'success': False}), 405, {'ContentType':'application/json'}
    img_data = None
    image_id = None
    if files and allowed_file(files.filename):
        filename = secure_filename(files.filename)
        files.save(os.path.join(UPLOAD_FOLDER, filename))
        img_data = plt.imread(os.path.join(UPLOAD_FOLDER, filename))
    if not img_data is None: 
        image_id = fs_obj.upload_image(img_data)
        image_url = request.host_url[0:-1] + url_for('static', filename=filename)
        
    if image_id is None:
        return json.dumps({'success': True}), {'ContentType':'application/json'}

    result_json = {}
    result_json['image_id'] = image_id
    result_json['image_url'] = image_url
    return json.dumps(result_json) 

@app.route("/select/image/<string:image_id>")
def select_img(image_id):
    # Set the image and get information about selection
    image_data = fs_obj.set_image(image_id) 

    # Get URL for boxed faces image
    boxed_faces_img = image_data['img_data'] #image_data['face_image']
    img_name = 'boxed_faces.jpg'
    img_path = os.path.join(UPLOAD_FOLDER, img_name)
    scipy.misc.imsave(img_path, boxed_faces_img)
    boxed_faces_url = request.host_url[0:-1] + url_for('static', filename=img_name)
    
    # Format result
    result_json = {}
    result_json['faces'] = {}
    for face in image_data['faces']: 
        result_json['faces'][face] = [int(x) for x in image_data['faces'][face]['location']]
    result_json['boxed_faces'] = boxed_faces_url
    result_json['img_dims'] = [int(boxed_faces_img.shape[0]), int(boxed_faces_img.shape[1])]
    print(result_json)

    return json.dumps(result_json)
    
    
@app.route("/select/face/<string:face_id>")
def select_face(face_id): 
    # return images for each face available for replacement
    result_json = {}
    for image in fs_obj.images: 
        for face in fs_obj.images[image]['faces']:
            if face_id == face: 
                face_img = fs_obj.images[image]['faces'][face]['face_data']
                img_name = '%s-%s.jpg' % (image, face)
                img_path = os.path.join(UPLOAD_FOLDER, img_name)
                scipy.misc.imsave(img_path, face_img)
                face_url = request.host_url[0:-1] + url_for('static', filename=img_name)
                result_json[image] = face_url
    return json.dumps(result_json)

@app.route("/delete/<string:image_id>", methods=['DELETE'])
def delete_img(image_id): 
    # delete image
    fs_obj.delete_image(image_id)
    # return success
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route("/swap/<string:image_id>/<string:face_id>")
def swap_face(image_id, face_id): 
    # process request
    result_img = fs_obj.process_face(image_id, face_id)
    
    # save result 
    result_name = 'result.jpg' 
    result_path = os.path.join(UPLOAD_FOLDER, result_name)
    scipy.misc.imsave(result_path, result_img)
    
    # return resulting image URL
    result_json = {}
    result_json['result'] = request.host_url[0:-1] + url_for('static', filename=result_name)
    return json.dumps(result_json)
    
@app.route("/restart")
def restart(): 
    fs_obj.reset()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
        

server = wsgi.WSGIServer(("localhost", 8000), app)
server.serve_forever()

if __name__ == '__main__': 
    app.run()