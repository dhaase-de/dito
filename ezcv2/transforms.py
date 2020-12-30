import cv2

import ezcv2.data
import ezcv2.infos


def flip_channels(image):
    """
    Changes BGR channels to RGB channels and vice versa.
    """
    return cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB)


def resize(image, scale_or_size, interpolation_down=cv2.INTER_CUBIC, interpolation_up=cv2.INTER_CUBIC):
    if isinstance(scale_or_size, float):
        scale = scale_or_size
        return cv2.resize(src=image, dsize=None, dst=None, fx=scale, fy=scale, interpolation=interpolation_up if scale > 1.0 else interpolation_down)
    
    elif isinstance(scale_or_size, tuple) and (len(scale_or_size) == 2):
        target_size = scale_or_size
        current_size = ezcv2.infos.size(image)
        return cv2.resize(src=image, dsize=target_size, dst=None, fx=0.0, fy=0.0, interpolation=interpolation_up if all(target_size[n_dim] > current_size[n_dim] for n_dim in range(2)) else interpolation_down)
    
    else:
        raise ValueError("Expected a float (= scale factor) or a 2-tuple (= target size) for argument 'scale_or_size', but got type '{}'".format(type(scale_or_size)))


def colorize(image, colormap_name):
    """
    Colorize the `image` using the colormap identified by `colormap_name`.
    """

    return cv2.applyColorMap(src=image, userColor=ezcv2.data.colormap(name=colormap_name))