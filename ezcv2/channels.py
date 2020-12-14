def isgray(image):
    return (len(image.shape) == 2) or ((len(image.shape) == 3) and (image.shape[2] == 1))


def iscolor(image):
    return (len(image.shape) == 3) and (image.shape[2] == 3)