import numpy as np
import cv2
from cv_cw2.paths import BERNIE_JPEG
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter


def main():
    # read bernie as a gray image
    bernie: np.array = cv2.imread(BERNIE_JPEG, cv2.IMREAD_GRAYSCALE)
    bernie = gaussian_filter(bernie, 0.5)
    kps = cv2.cornerHarris(bernie, blockSize=7, ksize=3, k=0.04)
    kps = np.argwhere(kps > 0.001 * kps.max())  # thresholding occurs here.
    kps = [cv2.KeyPoint(x=float(pt[1]), y=float(pt[0]), _size=1) for pt in kps]  # instantiating the key points
    drawn = cv2.drawKeypoints(bernie, kps, None, color=(255, 0, 0))  # draw the key points here.
    plt.imshow(drawn, cmap="gray")
    plt.show()


if __name__ == '__main__':
    main()
