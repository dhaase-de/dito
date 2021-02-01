import cv2

import qv2.data


def colorize(image, colormap_name):
    """
    Colorize the `image` using the colormap identified by `colormap_name`.
    """

    return cv2.applyColorMap(src=image, userColor=qv2.data.colormap(name=colormap_name))