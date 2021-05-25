"""
Visualizing the effect of the sobel filter.
"""
import numpy as np
import cv2
from cv_cw2.paths import BERNIE_JPEG
import matplotlib.pyplot as plt
from scipy.ndimage import sobel


def main():
    # read bernie as a gray image
    bernie: np.array = cv2.imread(BERNIE_JPEG, cv2.IMREAD_GRAYSCALE)
    # this uses the reflect mode by default. - but still, not quite sure what that means ..
    bernie_dx = sobel(bernie, axis=1, mode="reflect")  # horizontal derivative; reveals vertical edges
    bernie_dy = sobel(bernie, axis=0, mode="reflect")  # vertical derivative; reveals horizontal edges
    _, axarr = plt.subplots(1, 2)
    axarr[0].imshow(bernie_dx, cmap='gray')
    axarr[1].imshow(bernie_dy, cmap='gray')
    plt.show()
    assert bernie.shape == bernie_dx.shape


if __name__ == '__main__':
    main()
