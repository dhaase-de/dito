import operator

import cv2
import numpy as np

import dito.core


##
## contours
##


class ContourFinder():
    def __init__(self, image):
        self.image = image.copy()
        if self.image.dtype == np.bool:
            self.image = dito.core.convert(image=self.image, dtype=np.uint8)
        self.contours = self.find_contours(image=self.image)

    def __len__(self):
        """
        Returns the number of found contours.
        """
        return len(self.contours)

    def __getitem__(self, key):
        return self.contours[key]

    @staticmethod
    def find_contours(image):
        """
        Called internally to find the contours in the given `image`.
        """

        # find raw contours
        result = cv2.findContours(image=image, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE)

        # compatible with OpenCV 3.x and 4.x, see https://stackoverflow.com/a/53909713/1913780
        contours_raw = result[-2]

        # return tuple of instances of class `Contour`
        return [Contour(points=contour_raw[:, 0, :]) for contour_raw in contours_raw]

    def filter(self, func, min_value=None, max_value=None):
        if (min_value is None) and (max_value is None):
            # nothing to do
            return

        # filter
        contours_filtered = []
        for contour in self.contours:
            value = func(contour)
            if (min_value is not None) and (value < min_value):
                continue
            if (max_value is not None) and (value > max_value):
                continue
            contours_filtered.append(contour)
        self.contours = contours_filtered

    def filter_area(self, min_value=None, max_value=None):
        self.filter(func=operator.methodcaller("area"), min_value=min_value, max_value=max_value)

    def filter_perimeter(self, min_value=None, max_value=None):
        self.filter(func=operator.methodcaller("area"), min_value=min_value, max_value=max_value)

    def find_largest(self, return_index=True):
        """
        Returns the index of the largest (area-wise) contour.
        """
        max_area = None
        argmax_area = None
        for (n_contour, contour) in enumerate(self.contours):
            area = contour.area()
            if (max_area is None) or (area > max_area):
                max_area = area
                argmax_area = n_contour

        if argmax_area is None:
            return None
        else:
            if return_index:
                return argmax_area
            else:
                return self.contours[argmax_area]


def contours(image):
    """
    Convenience wrapper for `ContourFinder`.
    """
    contour_finder = ContourFinder(image=image)
    return contour_finder.contours


class Contour():
    def __init__(self, points):
        self.points = points

    def __len__(self):
        """
        Returns the number of points.
        """
        return len(self.points)

    def center(self):
        return np.mean(self.points, axis=0)

    def area(self):
        return cv2.contourArea(contour=self.points, oriented=None)

    def perimeter(self):
        return cv2.arcLength(curve=self.points, closed=True)

    def draw(self, image, color, thickness=1, filled=True, antialias=False, offset=None):
        cv2.drawContours(image=image, contours=[self.points], contourIdx=0, color=color, thickness=cv2.FILLED if filled else thickness, lineType=cv2.LINE_AA if antialias else cv2.LINE_8, offset=offset)
