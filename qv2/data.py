import os.path

import cv2
import numpy as np

import qv2.io


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datafiles")
DATA_FILENAMES = {
    "image:PM5544": os.path.join(DATA_DIR, "images", "PM5544.png"),
    "colormap:plot": os.path.join(DATA_DIR, "colormaps", "plot.png"),
}


####
#%%% non-image data
####


def colormap(name):
    """
    Returns the colormap specified by `name` as NumPy array of size
    `(256, 1, 3)`.
    """
    
    # source 1: non-OpenCV colormaps ToDo
    data_key = "colormap:{}".format(name.lower())
    if data_key in DATA_FILENAMES.keys():
        return qv2.io.load(filename=DATA_FILENAMES[data_key])
    
    # source 2: OpenCV colormaps
    full_cv2_name = "COLORMAP_{}".format(name.upper())
    if hasattr(cv2, full_cv2_name):
        return cv2.applyColorMap(src=yslope(width=1), colormap=getattr(cv2, full_cv2_name))
    
    # no match
    raise ValueError("Unknown colormap '{}'".format(name))


####
#%%% real images
####


def pm5544():
    return qv2.io.load(filename=DATA_FILENAMES["image:PM5544"])


####
#%%% synthetic images
####


def xslope(height=32, width=256):
    """
    Return image containing values increasing from 0 to 255 along the x axis.
    """
    
    slope = np.linspace(start=0, stop=255, num=width, endpoint=True, dtype=np.uint8)
    slope.shape = (1,) + slope.shape
    slope = np.repeat(a=slope, repeats=height, axis=0)
    return slope


def yslope(width=32, height=256):
    """
    Return image containing values increasing from 0 to 255 along the y axis.
    """
    
    return xslope(height=width, width=height).T
