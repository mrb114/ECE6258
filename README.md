# ECE6258
Written by Mallory Busso, Elena Haag, and Caroline Seng

Installation
------------
This package uses Python2.7 and comes with a requirements.txt file. It is recommended to install this project in a virtual environment such as anaconda (recommended) or virtualenv. The following commands assume you have installed anaconda or virtualenv previously. To set up a virtual environment in a Unix/Linux environment using virtualenv run the following at the command line: 

```
virtualenv venv 
source venv/bin/activate 
```

Or for a  Windows environment: 

```
virtualenv venv
source venv/Scripts/activate
```

Or using Anaconda: 

```
conda create ece6258_env
source activate ece6258_env
```

To install dependencies directly related to this project, use the following command inside your virtual environment: 

```
pip install -r requirements.txt
```

or in Anaconda: 

```
conda install --file requirements.txt
```

This command should allow the user to install all development related dependencies with the exception of the "opencv" package. Opencv version 3.0.0 can be installed easily using Anaconda by using the following command: 

```
conda install -c menpo opencv3
```

If you are not using anaconda, please see Opencv's instruction page on how to install the package for your particular OS and environment. Instructions for Windows can be found here: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html or for Linux here: https://www.pyimagesearch.com/2016/12/19/install-opencv-3-on-macos-with-homebrew-the-easy-way/. If you are using a different environment, please seek instruction from Opencv's webpage (https://docs.opencv.org/3.0-beta/index.html) or from another source. 

Occasionally, Windows users can have difficulty getting the scipy package installed. If this is the case, it is recommended to download the precompiled Windows version here: https://www.lfd.uci.edu/~gohlke/pythonlibs/. Simply find the scipy package section, install the 2.7 version for your environment (i.e. 32 or 64 bit OS) and download the package. Once the package has been downloaded, use the following command to install it: 

```
pip install <path_to_scipy_download>
```

Usage
------

This package was designed to be the backend compute logic for a frontend application. The frontend application along with instructions on how to use it can be found here: https://github.com/mrb114/ECE6258-UI. It is recommended to use the front end application by hosting the backend using Flask. If you would prefer to use the python code without the frontend facilitating the usage, you may utilize the core processing components as noted below. 

### How to host the backend

Note: Please execute these commands from a command line within the src/ directory of this repository. 
```
export FLASK_APP=app.py
flask run
```
If you are using the cmd.exe within Windows, you may have to use ```set``` instead of ```export```. It is recommended, but not required, to use GitBash for execution of these commands in a Windows environment which can be found here: https://git-scm.com/downloads. 

These commands will start up the back end at localhost:8000. The back end will require usage of port 8000 on your system. Please terminate any other processes using this port prior to running the back end. Once running, the ```flask run``` command may appear to "hang". This behavior is normal as the backend is awaiting a call from the frontend. Please see the README associated with the front end (link above) for instructions on how to use the front end. At this point, your back end should be running and you are ready to use the front end to initiate your processing. If at any point you wish to kill the process, simply hit Ctrl+C in the terminal and the process will be terminated. 

### Example of python usage 

```
import Facial_Edge
import IStitch
import matplotlib.pyplot as plt
import scipy.misc

# Read in images 
bad_img = plt.imread("bad_img.jpg")
good_img = plt.imread("good_img.jpg")

# Detect faces in images - Select to swap out face at index 0
face = Facial_Edge.Facial_Edge(bad_img).identify().select_face(0).locate_face(good_img)

# Stitch the images together
stitch = IStitch.IStitch(np.float64(bad_img), face.new_face_mask, face.mask).stitch_img()

# Save resulting image
scipy.misc.imsave("resulting_img.jpg", stitch.stitched_img_)
```

Ideal Input
-----------

The processing implemented in this package was designed for use in fixing group photos that were taken in sequence where 1 or many people may have not smiled, closed their eyes, etc. This is not a generic face swapping tool to swap any face with any other in the image. The idea is to fix the group shot gone wrong with minimal traces within the final image. Ideal images will be "burst" photos or photos that were taken in sequence where the subjects of the image did not move significantly. Ideally the resolution between the images will be similar. The back end should handle as many images as supplied, however the front end is designed to work with four image samples and thus the back end has been primarily tested on sample sizes of four or less. Larger images will take more time to process. If you are seeing the loading screen on the front end for a significant amount of time, double check that you have not received an error message in the terminal running the back end. The uploaded images must be oriented properly, that is the images should not be rotated. If the images are not oriented properly, you are likely to get errors. The images will be shown in the front end application in the orientation they were supplied so if they are not correct in the front end application then you have not uploaded them in the proper orientation. You may attempt to run the application using non-ideal images, but this package follows the "garbage-in: garbage-out" mentality and will likely not work well (if at all) with images that don't follow these constraints. 

Implementation
--------------
Image Registration: 
* Image registration uses Opencv's Motion Homography 
* Opencv's registration is designed for 2D images (i.e. not color images) thus the color images used for the purposes of this application are first converted to grayscale images prior to computing the registration 
* As multiple floating images may be required to generate one successful group image, the image registration class, IReg, allows for multiple floating images to be uploaded at once and each will be registered individually to the reference image
* Future implementations may include multi-processing to improve processing time of the registration process

Facial Segmentation: 
* Haar cascades are used for detecting faces within images. The trained Haar cascades are available through Opencv and have been trained for "standard" and "profile" faces 
* Both cascades are used and the detected faces are compared and any duplicates are removed. By using both cascades, a wider variety of face types and orientations can be detected
* To compare faces, the cross correlation coefficient is computed between the identified faces. A face with a high correlation coefficent indicates that the faces are likely belonging to the same person. This metric is used to identify faces within images that are candidates for replacement. 

Image Stitching: 
* Image stitching is implemented using the mask created from the facial segmenation step with Gaussian pyramids. 
* OpenCV implementations of pyramid generations are utilized for the creation of the Gaussian and Laplacian pyramids. 

Development
-----------
When contributing to this repository please do the following: 
* Use flake8 linting tool 
* Update the requirements.txt file with any new dependencies 
* Include a description of your changes in the commit changes 
* Update this README to include any new information that may be helpful to other users/developers
