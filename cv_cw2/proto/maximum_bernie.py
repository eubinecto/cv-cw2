import numpy as np
import cv2
from cv_cw2.paths import BERNIE_JPEG
import matplotlib.pyplot as plt
from scipy.ndimage import maximum_filter


def main():
    # read bernie as a gray image
    bernie: np.array = cv2.imread(BERNIE_JPEG, cv2.IMREAD_GRAYSCALE)
    # this uses the reflect mode by default. - but still, not quite sure what that means ..
    bernie_max: np.array = maximum_filter(bernie, size=1500, mode="reflect")
    _, axarr = plt.subplots(1, 2)
    axarr[0].imshow(bernie, cmap='gray')
    axarr[1].imshow(bernie_max, cmap='gray')
    plt.show()
    assert bernie.shape == bernie_max.shape


if __name__ == '__main__':
    main()
