import cv2

import dito.core


def otsu(image):
    if dito.core.is_color(image=image):
        raise ValueError("Expected gray image but got color image for Otsu thresholding")
    (theta, image2) = cv2.threshold(src=image, thresh=-1, maxval=255, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return (theta, image2)


def otsu_theta(image):
    (theta, image2) = otsu(image=image)
    return theta


def otsu_image(image):
    (theta, image2) = otsu(image=image)
    return image2


def dilate(image, shape=cv2.MORPH_ELLIPSE, size=3, iterations=1):
    ksize = dito.utils.get_validated_tuple(x=size, type_=int, count=2)
    kernel = cv2.getStructuringElement(shape=shape, ksize=ksize, anchor=(-1, -1))
    return cv2.dilate(src=image, kernel=kernel, iterations=iterations)