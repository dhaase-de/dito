import functools
import os.path

import cv2
import numpy as np

import dito.utils


class CachedImageLoader():
    def __init__(self, max_count=128):
        # decorate here, because maxsize can be specified by the user
        self.load = functools.lru_cache(maxsize=max_count, typed=True)(self.load)

    def load(self, filename, color=None):
        return load(filename=filename, color=color)

    def get_cache_info(self):
        return self.load.cache_info()

    def clear_cache(self):
        self.load.cache_clear()


def load(filename, color=None):
    """
    Load image from file given by `filename` and return NumPy array.

    If `color` is `None`, the image is loaded as-is. If `color` is `False`, a
    grayscale image is returned. If `color` is `True`, then a color image is
    returned, even if the original image is grayscale.

    The bit-depth (8 or 16 bit) of the image file will be preserved.
    """

    # check if file exists
    if not os.path.exists(filename):
        raise FileNotFoundError("Image file '{}' does not exist".format(filename))

    if filename.endswith(".npy"):
        # use NumPy
        image = np.load(file=filename)
    else:
        # use OpenCV
        if color is None:
            # load the image as it is
            flags = cv2.IMREAD_ANYDEPTH | cv2.IMREAD_UNCHANGED
        else:
            # force gray/color mode
            flags = cv2.IMREAD_ANYDEPTH | (cv2.IMREAD_COLOR if color else cv2.IMREAD_GRAYSCALE)
        image = cv2.imread(filename=filename, flags=flags)
    
    # check if loading was successful
    if not isinstance(image, np.ndarray):
        raise TypeError("Could not load image from file '{}' (expected object ob type 'np.ndarray', but got '{}'".format(filename, type(image)))

    return image


def save(filename, image, mkdir=True):
    """
    Save image `image` to file `filename`.

    If `mkdir` is `True`, the parent dir of the given filename is created
    before saving the image.
    """

    if not isinstance(image, np.ndarray):
        raise RuntimeError("Invalid image (type '{}')".format(type(image).__name__))

    # create parent dir
    if mkdir:
        dito.utils.mkdir(dirname=os.path.dirname(filename))

    if filename.endswith(".npy"):
        # use NumPy
        np.save(file=filename, arr=image)
    else:
        # use OpenCV
        cv2.imwrite(filename=filename, img=image)


def decode(b, color=None):
    """
    Load image from the byte array `b` containing the *encoded* image and
    return NumPy array.

    If `color` is `None`, the image is loaded as-is. If `color` is `False`, a
    grayscale image is returned. If `color` is `True`, then a color image is
    returned, even if the original image is grayscale.

    The bit-depth (8 or 16 bit) of the image file will be preserved.
    """

    # byte array -> NumPy array
    buf = np.frombuffer(b, dtype=np.uint8)

    # flags - select grayscale or color mode
    if color is None:
        flags = cv2.IMREAD_UNCHANGED
    else:
        flags = cv2.IMREAD_ANYDEPTH | (cv2.IMREAD_COLOR if color else cv2.IMREAD_GRAYSCALE)

    # read image
    image = cv2.imdecode(buf=buf, flags=flags)

    return image


def encode(image, extension="png", params=None):
    """
    Encode the given `image` into a byte array which contains the same bytes
    as if the image would have been saved to a file.
    """

    # allow extensions to be specified with or without leading dot
    if not extension.startswith("."):
        extension = "." + extension

    # use empty tuple if no params are given
    if params is None:
        params = tuple()

    (_, array) = cv2.imencode(ext=extension, img=image, params=params)

    return array.tobytes()
