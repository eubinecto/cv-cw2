from typing import List
import cv2
import numpy as np
from cv_cw2.paths import BERNIE_JPEG
from cv_cw2.task_1 import harris_points_detector


# instantiate an ORB here. to be used by the two functions below.
orb = cv2.ORB_create()


def feature_descriptor(image: np.ndarray, kps: List[cv2.KeyPoint]) -> np.ndarray:
    global orb
    _, des = orb.compute(image, kps)  # why does this crash?
    return des


def main():
    bernie = cv2.imread(BERNIE_JPEG, cv2.IMREAD_GRAYSCALE)
    # compare the results here.
    kps = harris_points_detector(bernie, 0.5)
    des = feature_descriptor(bernie, kps)  # just checking if this works
    print(des.shape)  # should be: (num_kps, feature_size)


if __name__ == '__main__':
    main()
