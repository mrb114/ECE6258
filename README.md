# ECE6258
ECE6258 project 
Written by Mallory Busso, Elena Haag, and Caroline Seng

Installation
------------
This package comes with a requirements.txt file. It is recommended to install this project in a virtual environment such as anaconda or virtual env. The following commands assume you have installed anaconda or virtualenv previously. To set up a virtualenv try in a Unix/Linux environment: 

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

This command should allow the user to install all development related dependencies. 

Usage
------

Example of image registration usage. Note: processing may take several minutes to complete 
```
import IReg
from matplotlib.pyplot import plt

# Read in images (expected to be of same size)
referenceImage = plt.imread('Reference_Image.png')
floatingImage = plt.imread('Floating_image.png')

# Apply registration to floating image
regObj = IReg.IReg(referenceImage, floatingImage).register()

# View registered image
plt.figure()
plt.imshow(regObj.float['Image0']['registered'])

```

Implementation
--------------
Image Registration: 
* Image registration uses the BSD licensed imreg_dft created by Matěj Týč and Christoph Gohlke which implements DFT based image registration (http://pythonhosted.org/imreg_dft/)
* The imreg_dft package is designed for 2D images (i.e. not color images) thus the color images used for the purposes of this application must be handled separately 
* To accomodate the color images, the registration transformation is computed for each channel of the input volumes and averaged across the R, G, and B channels before being applied to the float image 
* As multiple floating images may be required to generate one successful group image, the image registration class, IReg, allows for multiple floating images to be uploaded at once and each will be registered individually to the reference image
* Future implementations will include multi-processing to improve processing time of the registration process

Development
-----------
When contributing to this repository please do the following: 
* Use flake8 linting tool 
* Update the requirements.txt file with any new dependencies 
* Include a description of your changes in the commit changes 
* Update this README to include any new information that may be helpful to other users/developers
