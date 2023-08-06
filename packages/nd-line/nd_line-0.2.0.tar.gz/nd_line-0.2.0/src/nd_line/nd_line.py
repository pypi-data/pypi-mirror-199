"""Module for creating an n-dimensional line.

Copyright Daniel Marshall
"""
import math
from typing import List, Optional

import numpy as np
from numpy import ndarray
from numpy.typing import ArrayLike
from scipy.interpolate import splev, splprep


class nd_line:
    """Class for n-dimensional line."""

    def __init__(self, points: ArrayLike) -> None:
        """Create a line from a list of points.

        :param points: list of points
        """
        self.points = np.array([tuple(x) for x in points])
        alldist = self._lengths(self.points)
        self.length = sum(alldist)
        self.cumul: ndarray = np.cumsum([0.0] + alldist)
        self.type = 'linear'

    def _lengths(self, points: ndarray) -> List[float]:
        """Calculate the length (sum of the euclidean distance between points).

        :param points: numpy array of points
        :return: length of the line
        """
        return [self.e_dist(points[i], points[i + 1]) for i in range(len(points) - 1)]

    def _length(self, points: ndarray) -> float:
        """Calculate the length (sum of the euclidean distance between points).

        :param points: numpy array of points
        :type points: ndarray
        :return: length of the line
        """
        return sum([self.e_dist(points[i], points[i + 1]) for i in range(len(points) - 1)])

    def interp(self, dist: float) -> ndarray:
        """Return a point a specified distance along the line.

        :param dist: distance along the line
        :type dist: float
        :return: numpy array of the point coordinates
        """
        assert dist <= self.length, 'length cannot be greater than line length'
        assert dist >= 0, 'length cannot be less than zero'
        if dist == 0:
            return self.points[0]
        if dist == self.length:
            return self.points[-1]
        index = np.where(self.cumul < dist)[0][-1]
        d = self.cumul[index]
        vector = (self.points[index + 1] - self.points[index]) / self.e_dist(self.points[index], self.points[index + 1])
        remdist = dist - d
        final_point = remdist * vector + self.points[index]
        return final_point

    def interp_rat(self, ratio: float) -> ndarray:
        """Return a point a specified ratio along the line.

        :param ratio: ratio along the line
        :return: numpy array of the point coordinates
        """
        assert ratio <= 1, "Ratio for interp_rat() must be a value from 0 to 1"
        return self.interp(ratio * self.length)

    def splineify(self, samples: Optional[int] = None, s: float = 0) -> None:
        """Turn line into a spline approximation, currently occurs in place.

        :param samples: number of samples to use for spline approximation
        :param s: smoothing factor for spline approximation
        """
        if samples is None:
            samples = len(self.points)
        tck, u, _, _, _ = splprep([self.points[:, i] for i in range(self.points.shape[1])], s=s)
        self.points = np.transpose(splev(np.linspace(0, 1, num=samples), tck))
        self.length = self._length(self.points)
        self.type = 'spline'

    @staticmethod
    def e_dist(a: ndarray, b: ndarray) -> float:
        """Calculate the euclidean distance between two points.

        :param a: numpy array of point a
        :param b: numpy array of point b
        :return: euclidean distance between a and b
        """
        return math.sqrt(sum((a - b) ** 2))
