from typing import List, Set, Tuple
import cv2
import numpy as np
from tqdm import tqdm
import argparse
from cv_cw2.paths import BERNIE_JPEG
from scipy.ndimage import sobel, gaussian_filter
import matplotlib.pyplot as plt

# --- constants --- #
WINDOW_SIZE = 5  # the gaussian filter size must be 5 by 5.
SIGMA = 2  # with the sigma of value 2.
LOCAL_WINDOW_SIZE = 7


# task 1
# key point params: x, y, size, angle.
def harris_points_detector(image: np.array, thresh_pre: float) -> List[cv2.KeyPoint]:
    """
    This should return an array of locations (with orientations),
    that can be read by the ORB `compute` function in openCV.
    the following functions may be useful:
    scipy.ndimage.sobel: filters the input image with sobel filter
    scipy.ndimage.gaussian_filter: filter with a gaussian filter
    :return:
    """
    global WINDOW_SIZE, SIGMA, LOCAL_WINDOW_SIZE
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
    for row_idx in tqdm(range(corner_mat.shape[0])):
        for col_idx in range(corner_mat.shape[1]):
            Ixx_win = Ixx_padded[row_idx: row_idx + WINDOW_SIZE, col_idx: col_idx + WINDOW_SIZE]
            Iyy_win = Iyy_padded[row_idx: row_idx + WINDOW_SIZE, col_idx: col_idx + WINDOW_SIZE]
            Ixy_win = Ixy_padded[row_idx: row_idx + WINDOW_SIZE, col_idx: col_idx + WINDOW_SIZE]
            # sum them up
            Sxx = Ixx_win.sum()
            Syy = Iyy_win.sum()
            Sxy = Ixy_win.sum()
            # this will take quite some time.
            # get the weight
            w = image_w[row_idx, col_idx]  # (2296, 2371)
            # now save the corner strength
            det = ((w**2) * Sxx * Syy) - ((w**2) * (Sxy**2))  # ad * bc
            trace = Sxx + Syy  # sum along the diagonal.
            corner_mat[row_idx, col_idx] = det - 0.1 * (trace**2)  # the corner strength function
    # --- compute the angles of the points as well --- #
    angles_mat = np.arctan2(image_dy, image_dx)  # use arctan2 instead of arctan. (quadrant)
    np.nan_to_num(angles_mat, nan=0.0)  # replace any non values with zeroes.
    thresh_post = thresh_pre * corner_mat.max()
    print("the thresh value:", thresh_post)
    # --- search for the local maxima --- #
    kps: Set[Tuple[int, int]] = set()
    for row_idx in tqdm(range(corner_mat.shape[0] - LOCAL_WINDOW_SIZE)):
        for col_idx in range(corner_mat.shape[1] - LOCAL_WINDOW_SIZE):
            window = corner_mat[row_idx: row_idx + LOCAL_WINDOW_SIZE, col_idx: col_idx + LOCAL_WINDOW_SIZE]
            if window.max() > thresh_post:  # thresholding occurs here
                max_kp = np.unravel_index(window.argmax(), window.shape)
                kps.add((max_kp[0] + row_idx, max_kp[1] + col_idx))
    # --- then select local maxima --- #
    return [
        # x, y, size, angle.
        cv2.KeyPoint(x=float(kp[1]),  # the column indices are the x values
                     y=float(kp[0]),  # the row indices are the y values
                     _size=1, _angle=angles_mat[kp[0], kp[1]])
        for kp in kps
    ]


# -- - utils --- #
def eval_truncate(sigma: float, filter_size: int) -> float:
    """
    evaluate the value of truncate given the values of sigma and kernel size.
    https://stackoverflow.com/questions/25216382/gaussian-filter-in-scipy
    :return:
    """
    return (((filter_size - 1)/2)-0.5)/sigma


def main():
    # first, read the image as a numpy array
    parser = argparse.ArgumentParser()
    parser.add_argument("--thresh_pre", type=float,
                        default=0.3)
    args = parser.parse_args()
    thresh_pre: float = args.thresh_pre
    # read the image
    bernie = cv2.imread(BERNIE_JPEG, cv2.IMREAD_GRAYSCALE)
    # 0.01, 0.1, 0.3.
    kps = harris_points_detector(bernie, thresh_pre)  # do this later. for now, use a built in harris.
    drawn = cv2.drawKeypoints(bernie, kps, None, color=(255, 0, 0))  # draw the key points here.
    plt.imshow(drawn, cmap="gray")
    plt.show()


if __name__ == '__main__':
    main()
