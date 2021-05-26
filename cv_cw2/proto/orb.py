"""
what the hell is an ORB detector?
"""
import numpy as np
import cv2
from cv_cw2.paths import BERNIE_JPEG
import matplotlib.pyplot as plt


def main():
    bernie: np.ndarray = cv2.imread(BERNIE_JPEG, cv2.IMREAD_GRAYSCALE)
    # Initiate ORB detector
    # don't use cv2.ORB() - that will crash.
    # https://stackoverflow.com/a/60478312
    orb = cv2.ORB_create()
    # find the keypoints with ORB
    kps = orb.detect(bernie, None)
    # compute the descriptors with ORB
    kps, des = orb.compute(bernie, kps)  # what the heck are the "descriptors" by the way?
    # draw only keypoints location, not size and orientation
    drawn = cv2.drawKeypoints(bernie, kps, None, color=(255, 0, 0), flags=0)
    plt.imshow(drawn)
    plt.show()


if __name__ == '__main__':
    main()
