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
        return tuple(Contour(points=contour_raw[:, 0, :]) for contour_raw in contours_raw)


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
