import numpy as np
import cv2
from cv_cw2.paths import BERNIE_JPEG
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter


def main():
    # read bernie as a gray image
    bernie: np.array = cv2.imread(BERNIE_JPEG, cv2.IMREAD_GRAYSCALE)
    # this uses the reflect mode by default. - but still, not quite sure what that means ..
    bernie_w: np.array = gaussian_filter(bernie, sigma=0.5, mode="reflect")  # horizontal derivative; reveals vertical edges
    _, axarr = plt.subplots(1, 2)
    axarr[0].imshow(bernie, cmap='gray')
    axarr[1].imshow(bernie_w, cmap='gray')
    plt.show()
    print(bernie_w[1, 1])


if __name__ == '__main__':
    main()
