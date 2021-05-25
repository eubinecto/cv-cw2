import numpy as np
import cv2
from cv_cw2.paths import BERNIE_JPEG
import matplotlib.pyplot as plt


def main():
    # read bernie as a gray image
    bernie: np.array = cv2.imread(BERNIE_JPEG, cv2.IMREAD_GRAYSCALE)
    plt.imshow(bernie, cmap='gray')
    plt.show()


if __name__ == '__main__':
    main()
