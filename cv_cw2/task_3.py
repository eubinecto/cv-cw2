import os
from typing import List
import cv2
import numpy as np
from cv_cw2.paths import BERNIES_DIR


def ssd_feature_matcher():
    """
    now the problem is this...
    """
    # TODO: implement this.. to match
    # use cv2.drawMatches()
    pass


def ratio_feature_matcher():
    pass


# --- utils --- #
def load_bernies() -> List[np.ndarray]:
    bernie_paths = [
        os.path.join(BERNIES_DIR, file_name)
        for file_name in os.listdir(BERNIES_DIR)
    ]
    # load all of them in numpy arrays
    return [
        cv2.imread(bernie_path, cv2.IMREAD_GRAYSCALE)
        for bernie_path in bernie_paths
    ]


def main():
    pass


if __name__ == '__main__':
    main()
