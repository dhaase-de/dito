import cv2
import numpy as np

import qv2.core
import qv2.data


def is_colormap(colormap):
    """
    Returns `True` iff `colormap` is a OpenCV-compatible colormap.
    
    For this, `colormap` must be a `uint8` array of shape `(256, 1, 3)`, i.e.
    a color image of size `1x256`.
    """
    if not qv2.core.is_image(image=colormap):
        return False
    if colormap.dtype != np.uint8:
        return False
    if colormap.shape != (256, 1, 3):
        return False
    return True


def colorize(image, colormap):
    """
    Colorize the `image` using the colormap identified by `colormap_name`.
    """
    if isinstance(colormap, str):
        return cv2.applyColorMap(src=image, userColor=qv2.data.colormap(name=colormap))
    elif is_colormap(colormap=colormap):
        return cv2.applyColorMap(src=image, userColor=colormap)
    else:
        raise TypeError("Argument `colormap` must either be a string (the colormap name) or a valid colormap.")