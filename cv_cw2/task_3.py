import os
from typing import List, Tuple
import cv2
import numpy as np
from scipy.spatial.distance import cdist
from cv_cw2.paths import VARS_DIR
from cv_cw2.task_1 import harris_points_detector
from cv_cw2.task_2 import feature_descriptor


class FeatureMatcher:

    def matchFeatures(self, feat_1: np.ndarray, feat_2: np.ndarray) -> List[cv2.DMatch]:
        """
        note: DMatch (int _queryIdx, int _trainIdx, float _distance)
        You should set the queryIdx attribute to the index of the feature in the first image,
        the trainIdx attribute to the index of the feature in the second image and the distance attribute to the
        distance between the two features as defined by the particular distance metric (e.g., SSD or ratio).
        """
        raise NotImplementedError


class SSDFeatureMatcher(FeatureMatcher):

    def matchFeatures(self, feat_1: np.ndarray, feat_2: np.ndarray) -> List[cv2.DMatch]:



class RatioFeatureMatcher(FeatureMatcher):

    def match_features(self, mode: str) -> List[cv2.DMatch]:
        kps, feats = self.extract(mode)


# --- utils --- #
def load_vars() -> List[np.ndarray]:

    var_paths = [
        os.path.join(VARS_DIR, file_name)
        for file_name in os.listdir(VARS_DIR)
    ]
    # load all of them in numpy arrays
    return [
        cv2.imread(var_path, cv2.IMREAD_GRAYSCALE)
        for var_path in var_paths
    ]


def main():
    # and also.. compare the performance of your harris corner & orb detect.
    #
    # cv2.drawMatches - for visualising the results
    pass


if __name__ == '__main__':
    main()
