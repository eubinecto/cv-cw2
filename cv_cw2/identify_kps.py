from typing import List
import cv2
import numpy as np
import argparse
from cv_cw2.paths import BERNIE_JPEG
from scipy.ndimage import sobel, maximum_filter, convolve
import matplotlib.pyplot as plt

# --- constants --- #
GAUSSIAN_WINDOW = 5  # the gaussian filter size must be 5 by 5.
SIGMA = 0.5  # with the sigma of value 0.5.
LOCAL_MAX_WINDOW = 7  # the local maximum filter size.


# task 1
# key point params: x, y, size, angle.
def harris_points_detector(image: np.array, thresh: float) -> List[cv2.KeyPoint]:
    """
    This should return an array of locations (with orientations),
    that can be read by the ORB `compute` function in openCV.
    the following functions may be useful:
    scipy.ndimage.sobel: filters the input image with sobel filter
    scipy.ndimage.gaussian_filter: filter with a gaussian filter
    :return:
    """
    global GAUSSIAN_WINDOW, SIGMA, LOCAL_MAX_WINDOW
    # --- normalize the image, first! --- #
    image = image.astype(np.float32)
    image /= image.max()  # we should first normalize the image, so that the value sits [0, 1]
    # --- compute the gradients --- #
    image_dx = sobel(image, axis=1, mode="reflect")  # grads with respect to x (horizontal convolution)
    image_dy = sobel(image, axis=0, mode="reflect")   # grads with respect to y (vertical convolution)
    # --- compute the components of the harris matrix --- #
    Ixx = image_dx**2
    Iyy = image_dy**2
    Ixy = image_dx * image_dy
    # --- get the gaussian-weighted sums ---- #
    # we don't need a nested for loop here. convolving over the image with a gaussian filter of 5 by 5 size
    # evaluates the harris matrix for me.
    kernel1d = cv2.getGaussianKernel(GAUSSIAN_WINDOW, SIGMA)
    kernel2d = np.outer(kernel1d, kernel1d.transpose())
    SIxx = convolve(Ixx, kernel2d, mode="reflect")  # sum up. (gaussian-weighted)
    SIyy = convolve(Iyy, kernel2d, mode="reflect")  # sum up. (gaussian-weighted)
    SIxy = convolve(Ixy, kernel2d, mode="reflect")  # sum up. (gaussian-weighted)
    # --- compute the corner strengths --- #
    det = SIxx * SIyy - (SIxy**2)
    trace = SIxx + SIyy
    corner_mat = det - 0.1 * (trace**2)  # the corner strengths
    # --- compute the angles of the points as well --- #
    angles_mat = np.arctan2(image_dy, image_dx)
    np.nan_to_num(angles_mat, nan=0.0)  # replace any non values with zeroes.
    # --- search for the local maxima --- #
    # the maximum filter will max-pool the original image.
    # if we equate the max-pooled with the original image, then we can reveal
    # the position of the local maxima. (i.e. the position of the True values)
    maxima_mat = (corner_mat == maximum_filter(corner_mat, size=LOCAL_MAX_WINDOW, mode="reflect"))
    # --- threshold the maxima and collect key points --- #
    kps: List[cv2.KeyPoint] = list()  # collect theses
    for row_idx in range(maxima_mat.shape[0]):  # row
        for col_idx in range(maxima_mat.shape[1]):  # col
            # if the position is the local maxima
            if maxima_mat[row_idx, col_idx]:
                # and if this is greater than or equal to the threshold
                if corner_mat[row_idx, col_idx] >= thresh:
                    # this is a key point
                    kp = cv2.KeyPoint(x=float(col_idx),  # the column indices are the x values
                                      y=float(row_idx),  # the row indices are the y values
                                      _size=1, _angle=angles_mat[row_idx, col_idx])
                    kps.append(kp)
    return kps  # return the key points


def main():
    # first, read the image as a numpy array
    parser = argparse.ArgumentParser()
    parser.add_argument("--thresh", type=float,
                        default=0.01)
    # parse args
    args = parser.parse_args()
    thresh: float = args.thresh

    # read the image
    bernie = cv2.imread(BERNIE_JPEG, cv2.IMREAD_GRAYSCALE)
    # 0.01, 0.1, 0.3.
    kps = harris_points_detector(bernie, thresh)  # do this later. for now, use a built in harris.
    print("num of kps:", len(kps))
    drawn = cv2.drawKeypoints(bernie, kps, None, color=(255, 0, 0))  # draw the key points here.
    plt.imshow(drawn, cmap="gray")
    plt.show()


if __name__ == '__main__':
    main()
