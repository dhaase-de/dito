import cv2

import qv2.infos


def otsu(image):
    if qv2.infos.is_color(image=image):
        raise ValueError("Expected gray image but got color image for Otsu thresholding")
    (theta, image2) = cv2.threshold(src=image, thresh=-1, maxval=255, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return (theta, image2)


def otsu_theta(image):
    (theta, image2) = otsu(image=image)
    return theta


def otsu_image(image):
    (theta, image2) = otsu(image=image)
    return image2
