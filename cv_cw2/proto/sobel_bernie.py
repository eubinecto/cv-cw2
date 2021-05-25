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
    bernie_sobel = sobel(bernie)
    _, axarr = plt.subplots(1, 2)
    axarr[0].imshow(bernie, cmap='gray')
    axarr[1].imshow(bernie_sobel, cmap='gray')
    plt.show()


if __name__ == '__main__':
    main()
