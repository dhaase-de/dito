import operator

import cv2
import numpy as np

import dito.core


##
## contours
##


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

    def center_x(self):
        return np.mean(self.points[:, 0])

    def center_y(self):
        return np.mean(self.points[:, 1])

    def area(self):
        return cv2.contourArea(contour=self.points, oriented=None)

    def perimeter(self):
        return cv2.arcLength(curve=self.points, closed=True)

    def circularity(self):
        r_area = np.sqrt(self.area() / np.pi)
        r_perimeter = self.perimeter() / (2.0 * np.pi)
        return r_area / r_perimeter

    def moments(self):
        return cv2.moments(array=self.points, binaryImage=False)

    def hu_moments(self, log=True):
        hu_moments = cv2.HuMoments(m=self.moments())
        if log:
            return np.sign(hu_moments) * np.log10(np.abs(hu_moments))
        else:
            return hu_moments

    def draw(self, image, color, thickness=1, filled=True, antialias=False, offset=None):
        cv2.drawContours(image=image, contours=[np.round(self.points).astype(np.int)], contourIdx=0, color=color, thickness=cv2.FILLED if filled else thickness, lineType=cv2.LINE_AA if antialias else cv2.LINE_8, offset=offset)


class ContourList():
    def __init__(self, contours):
        self.contours = contours

    def __len__(self):
        """
        Returns the number of found contours.
        """
        return len(self.contours)

    def __getitem__(self, key):
        return self.contours[key]

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

    def filter_center_x(self, min_value=None, max_value=None):
        self.filter(func=operator.methodcaller("center_x"), min_value=min_value, max_value=max_value)

    def filter_center_y(self, min_value=None, max_value=None):
        self.filter(func=operator.methodcaller("center_y"), min_value=min_value, max_value=max_value)

    def filter_area(self, min_value=None, max_value=None):
        self.filter(func=operator.methodcaller("area"), min_value=min_value, max_value=max_value)

    def filter_perimeter(self, min_value=None, max_value=None):
        self.filter(func=operator.methodcaller("area"), min_value=min_value, max_value=max_value)

    def filter_circularity(self, min_value=None, max_value=None):
        self.filter(func=operator.methodcaller("circularity"), min_value=min_value, max_value=max_value)

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

    def draw_all(self, image, colors=None, **kwargs):
        if colors is None:
            colors = tuple(dito.random_color() for _ in range(len(self)))

        for (contour, color) in zip(self.contours, colors):
            contour.draw(image=image, color=color, **kwargs)


class ContourFinder(ContourList):
    def __init__(self, image):
        self.image = image.copy()
        if self.image.dtype == np.bool:
            self.image = dito.core.convert(image=self.image, dtype=np.uint8)
        contours = self.find_contours(image=self.image)
        super().__init__(contours=contours)

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


def contours(image):
    """
    Convenience wrapper for `ContourFinder`.
    """
    contour_finder = ContourFinder(image=image)
    return contour_finder.contours


class VoronoiPartition(ContourList):
    def __init__(self, image_size, points):
        contours = self.get_facets(image_size=image_size, points=points)
        super().__init__(contours=contours)

    @staticmethod
    def get_facets(image_size, points):
        subdiv = cv2.Subdiv2D((0, 0, image_size[0], image_size[1]))
        for point in points:
            subdiv.insert(pt=point)
        (voronoi_facets, voronoi_centers) = subdiv.getVoronoiFacetList(idx=[])
        return [Contour(voronoi_facet) for voronoi_facet in voronoi_facets]


def voronoi(image_size, points):
    voronoi_partition = VoronoiPartition(image_size=image_size, points=points)
    return voronoi_partition.contours
