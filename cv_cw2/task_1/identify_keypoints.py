import numpy as np
from scipy.ndimage import sobel, gaussian_filter


def harris_points_detector(image: np.array) -> np.array:
    """
    This should return an array of locations (with orientations),
    that can be read by the ORB `compute` function in openCV.
    the following functions may be useful:
    scipy.ndimage.sobel: filters the input image with sobel filter
    scipy.ndimage.gaussian_filter: filter with a gaussian filter
    :return:
    """
    pass


def main():
    pass


if __name__ == '__main__':
    main()
