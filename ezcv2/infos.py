import collections

import cv2
import numpy as np

import ezcv2.utils


def is_image(image):
    """
    Return `True` iff the given image is either a valid grayscale image or a
    valid color image.
    """
    
    return is_gray(image=image) or is_color(image=image)
    

def is_gray(image):
    """
    Return `True` iff the given image is a grayscale image.
    """
    
    return (len(image.shape) == 2) or ((len(image.shape) == 3) and (image.shape[2] == 1))


def is_color(image):
    """
    Return `True` iff the given image is a color image.
    """
    
    return (len(image.shape) == 3) and (image.shape[2] == 3)


def as_gray(image):
    """
    Convert the given image from BGR to grayscale.
    
    If it is already a grayscale image, return the image unchanged.
    """
    
    if is_gray(image=image):
        return image
    else:
        return cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)


def as_color(image):
    """
    Convert the given image from grayscale to BGR.
    
    If it is already a color image, return the image unchanged.
    """
    
    if is_color(image=image):
        return image
    else:
        return cv2.cvtColor(src=image, code=cv2.COLOR_GRAY2BGR)


def size(image):
    """
    Return the size `(X, Y)` of the given image.
    """
    return (image.shape[1], image.shape[0])


def info(image):
    """
    Returns an ordered dictionary containing info about the given image.
    """

    result = collections.OrderedDict()
    result["size (KiB)"] = image.size * image.itemsize / 1024.0
    result["shape"] = image.shape
    result["dtype"] = image.dtype
    result["mean"] = np.mean(image)
    result["std"] = np.std(image)
    result["min"] = np.min(image)
    result["1st quartile"] = np.percentile(image, 25.0)
    result["median"] = np.median(image)
    result["3rd quartile"] = np.percentile(image, 75.0)
    result["max"] = np.max(image)
    return result


def pinfo(image):
    """
    Prints info about the given image.
    """
    
    result = info(image=image)
    ezcv2.utils.ptable(rows=result.items())


def hist(image, bin_count=256):
    """
    Return the histogram of the specified image.
    """
    
    # determine which channels to use
    if ezcv2.is_gray(image):
        channels = [0]
    elif ezcv2.is_color(image):
        channels = [0, 1, 2]
    else:
        raise ValueError("The given image must be a valid gray scale or color image")
    
    # accumulate histogram over all channels
    hist = sum(cv2.calcHist([image], [channel], mask=None, histSize=[bin_count], ranges=(0, 256)) for channel in channels)
    hist = np.squeeze(hist)
    
    return hist
    

def phist(image, bin_count=25, height=8, bar_symbol="#", background_symbol=" ", col_sep="."):
    """
    Print the histogram of the given image.
    """
    
    h = hist(image=image, bin_count=bin_count)
    h = h / np.max(h)
    
    print("^")
    for n_row in range(height):
        col_strs = []
        for n_bin in range(bin_count):
            if h[n_bin] > (1.0 - (n_row + 1) / height):
                col_str = bar_symbol
            else:
                col_str = background_symbol
            col_strs.append(col_str)
        print("|" + col_sep.join(col_strs))
    print("+" + "-" * ((bin_count - 1) * (1 + len(col_sep)) + 1) + ">")
