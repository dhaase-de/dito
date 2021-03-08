import cv2
import numpy as np


####
#%%% general
####


def is_image(image):
    """
    Return `True` iff the given image is either a valid grayscale image or a
    valid color image.
    """
    
    return is_gray(image=image) or is_color(image=image)


####
#%%% type-related
####


def dtype_range(dtype):
    """
    Returns the min and max intensity value of images for a given NumPy dtype.
    
    For integer dtypes, this corresponds to their full range.
    For floating dtypes, this corresponds to the range `(0.0, 1.0)`.
    For bool dtypes, this corresponds to the range (`False`, `True`).
    """
    if np.issubdtype(dtype, np.integer):
        info = np.iinfo(dtype)
        return (info.min, info.max)
    elif np.issubdtype(dtype, np.floating):
        return (0.0, 1.0)
    elif np.issubdtype(dtype, np.bool_):
        return (False, True)
    else:
        raise TypeError("Invalid dtype '{}'".format(dtype))


def convert(image, dtype):
    pass

####
#%%% array access
####


def tir(*args):
    """
    The items of `*args` are rounded, converted to `int` and combined into a
    tuple.

    The primary use-case of this function is to pass point coordinates to
    certain OpenCV functions.

    >>> tir(1.24, -1.87)
    (1, -2)
    """
    
    if (len(args) == 1) and (len(args[0]) == 2):
        items = args[0]
    elif len(args) == 2:
        items = args
    else:
        raise ValueError("The two required arguments must either be (i) given separately or (ii) via a sequence of length two, but got neither")
    return tuple(int(round(item)) for item in items)


####
#%%% size-related
####


def size(image):
    """
    Return the size `(X, Y)` of the given image.
    """
    return (image.shape[1], image.shape[0])


def resize(image, scale_or_size, interpolation_down=cv2.INTER_CUBIC, interpolation_up=cv2.INTER_CUBIC):
    if isinstance(scale_or_size, float):
        scale = scale_or_size
        return cv2.resize(src=image, dsize=None, dst=None, fx=scale, fy=scale, interpolation=interpolation_up if scale > 1.0 else interpolation_down)
    
    elif isinstance(scale_or_size, tuple) and (len(scale_or_size) == 2):
        target_size = scale_or_size
        current_size = size(image)
        return cv2.resize(src=image, dsize=target_size, dst=None, fx=0.0, fy=0.0, interpolation=interpolation_up if all(target_size[n_dim] > current_size[n_dim] for n_dim in range(2)) else interpolation_down)
    
    else:
        raise ValueError("Expected a float (= scale factor) or a 2-tuple (= target size) for argument 'scale_or_size', but got type '{}'".format(type(scale_or_size)))


####
#%%% channel-related
####
    

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


def flip_channels(image):
    """
    Changes BGR channels to RGB channels and vice versa.
    """
    return cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB)

####
#%%% value-related
####


def clip(image, lower=None, upper=None):
    """
    Clip values to the range specified by `lower` and `upper`.
    """
    if lower is not None:
        image[image < lower] = lower
    if upper is not None:
        image[image > upper] = upper
    return image


def clip_01(image):
    """
    Clip values to the range `(0.0, 1.0)`.
    """
    return clip(image=image, lower=0.0, upper=1.0)


def clip_11(image):
    """
    Clip values to the range `(-1.0, 1.0)`.
    """
    return clip(image=image, lower=-1.0, upper=1.0)


def normalize(image, mode="minmax", **kwargs):
    """
    Normalizes the intensity values of the given image.
    """

    if mode == "none":
        return image

    elif mode == "interval":
        # interval range to be spread out to the "full" interval range
        (lower_source, upper_source) = sorted((kwargs["lower"], kwargs["upper"]))

        # the target interval range depends on the image's data type
        (lower_target, upper_target) = dtype_range(image.dtype)

        # we temporarily work with a float image (because values outside of
        # the target interval can occur)
        image_work = image.astype("float").copy()
        
        # spread the given interval to the full range, clip outlier values
        image_work = (image_work - lower_source) / (upper_source - lower_source) * (upper_target - lower_target) + lower_target
        image_work = clip(image=image_work, lower=lower_target, upper=upper_target)

        # return an image with the original data type
        return image_work.astype(image.dtype)

    elif mode == "minmax":
        return normalize(image, mode="interval", lower=np.min(image), upper=np.max(image))

    elif mode == "zminmax":
        # "zero-symmetric" minmax (makes only sense for float images)
        absmax = max(np.abs(np.min(image)), np.abs(np.max(image)))
        return normalize(image, mode="interval", lower=-absmax, upper=absmax)

    elif mode == "percentile":
        for key in ("q", "p"):
            if key in kwargs.keys():
                q = kwargs[key]
                break
        else:
            q = 2.0
        q = min(max(0.0, q), 50.0)
        return normalize(image, mode="interval", lower=np.percentile(image, q), upper=np.percentile(image, 100.0 - q))

    else:
        raise ValueError("Invalid mode '{mode}'".format(mode=mode))
