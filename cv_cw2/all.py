from typing import List, Set, Tuple
import cv2
import numpy as np
from tqdm import tqdm

from cv_cw2.paths import BERNIE_JPEG
from scipy.ndimage import sobel, gaussian_filter, maximum_filter
import matplotlib.pyplot as plt

# --- constants --- #
WINDOW_SIZE = 5  # the gaussian filter size must be 5 by 5.
SIGMA = 2  # with the sigma of value 2.


# task 1
# key point params: x, y, size, angle.
def harris_points_detector(image: np.array, thresh: int) -> List[cv2.KeyPoint]:
    """
    This should return an array of locations (with orientations),
    that can be read by the ORB `compute` function in openCV.
    the following functions may be useful:
    scipy.ndimage.sobel: filters the input image with sobel filter
    scipy.ndimage.gaussian_filter: filter with a gaussian filter
    :return:
    """
    global WINDOW_SIZE, SIGMA
    # --- compute the gradients --- #
    image_dx = sobel(image, axis=1, mode="reflect")  # grads with respect to x (horizontal)
    image_dy = sobel(image, axis=0, mode="reflect")   # grads with respect to y (vertical)
    # --- compute the components of the harris matrix --- #
    Ixx = image_dx**2
    Iyy = image_dy**2
    Ixy = image_dx * image_dy
    # # --- get the window weights ---- #
    image_w = gaussian_filter(image, sigma=SIGMA, truncate=eval_truncate(SIGMA, WINDOW_SIZE),
                              mode="reflect")  # for pixels outside image, reflect the edges.
    # # --- pad the variables before the convolution --- #
    Ixx_padded = np.pad(Ixx, (WINDOW_SIZE - 1, WINDOW_SIZE - 1), 'reflect')
    Iyy_padded = np.pad(Iyy, (WINDOW_SIZE - 1, WINDOW_SIZE - 1), 'reflect')
    Ixy_padded = np.pad(Ixy, (WINDOW_SIZE - 1, WINDOW_SIZE - 1), 'reflect')
    # ---  now compute the corner strength matrix --- #
    corner_mat = np.zeros(shape=image.shape)  # this is what we want
    for x_idx in tqdm(range(corner_mat.shape[0])):  # loop over the rows  # this will take quite a time.
        for y_idx in range(corner_mat.shape[1]):  # loop over the columns
            pass
            Ixx_win = Ixx_padded[x_idx: x_idx + WINDOW_SIZE, y_idx: y_idx + WINDOW_SIZE]
            Iyy_win = Iyy_padded[x_idx: x_idx + WINDOW_SIZE, y_idx: y_idx + WINDOW_SIZE]
            Ixy_win = Ixy_padded[x_idx: x_idx + WINDOW_SIZE, y_idx: y_idx + WINDOW_SIZE]
            # sum them up
            Sxx = np.sum(Ixx_win)
            Syy = np.sum(Iyy_win)
            Sxy = np.sum(Ixy_win)
            # get the weight
            w = image_w[x_idx, y_idx]
            # now save the corner strength
            det = (w * Sxx * w * Syy) - (w * Sxy * w * Sxy)  # ad * bc
            trace = Sxx + Syy  # sum along the diagonal.
            corner_mat[x_idx, y_idx] = det - 0.1 * (trace**2)  # the corner strength function
    # --- compute the angles of the points as well --- #
    angles_mat = np.arctan(image_dy / image_dx)
    # --- search for the local maxima --- #
    key_coords: Set[Tuple[int, int]] = set()
    for x_idx in tqdm(range(corner_mat.shape[0] - 7)):
        for y_idx in range(corner_mat.shape[1] - 7):
            # get the window
            window = corner_mat[x_idx: x_idx + 7, y_idx: y_idx + 7]
            max_coord = np.unravel_index(window.argmax(), window.shape)
            if corner_mat[max_coord[0], max_coord[1]] >= thresh:
                key_coords.add(max_coord)
    # --- then select local maxima --- #
    return [
        # x, y, size, angle.
        cv2.KeyPoint(x=float(key_coord[0]), y=float(key_coord[1]),  # these have to be float.. for some reason...
                     _size=1, _angle=int(angles_mat[key_coord[0], key_coord[1]]))
        for key_coord in key_coords
    ]


def eval_truncate(sigma: float, filter_size: int) -> float:
    """
    evaluate the value of truncate given the values of sigma and kernel size.
    https://stackoverflow.com/questions/25216382/gaussian-filter-in-scipy
    :return:
    """
    return (((filter_size - 1)/2)-0.5)/sigma


# task 2
def feature_descriptor(key_points: List[cv2.KeyPoint]):
    pass


# task 3 - 1
def ssd_feature_matcher():
    pass


# task 3 - 2
def ratio_feature_matcher():
    pass


def main():
    # first, read the image as a numpy array
    bernie = cv2.imread(BERNIE_JPEG, cv2.IMREAD_GRAYSCALE)
    # key_points = harris_points_detector(bernie, thresh=220)  # do this later. for now, use a built in harris.
    dst = cv2.cornerHarris(bernie, blockSize=2, ksize=3, k=0.04)
    kps = np.argwhere(dst > 0.1 * dst.max())  # thresholding occurs here.
    kps = [cv2.KeyPoint(x=float(pt[1]), y=float(pt[0]), _size=3) for pt in kps]  # instantiating the key points
    drawn = cv2.drawKeypoints(bernie, kps, bernie, color=(255, 0, 0))  # draw the key points here.
    plt.imshow(drawn, cmap="gray")
    plt.show()


if __name__ == '__main__':
    main()
