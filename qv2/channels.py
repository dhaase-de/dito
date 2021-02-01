import cv2


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


def flip_channels(image):
    """
    Changes BGR channels to RGB channels and vice versa.
    """
    return cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB)