import os
from typing import List, Tuple
import cv2
import numpy as np
from scipy.spatial.distance import cdist
import argparse
import matplotlib.pyplot as plt
from cv_cw2.identify_keypoints import harris_points_detector
from cv_cw2.paths import VARS_DIR, BERNIE_JPEG


class FeatureMatcher:

    def matchFeatures(self, descriptors_1: np.ndarray, descriptors_2: np.ndarray) -> List[cv2.DMatch]:
        """
        descriptors_1: [num_kps, num_descs] of an image (image 1)
        descriptors_2: [num_kps, num_descs] if another image (image 2)
        and... it returns the matches.
        note: DMatch (int _queryIdx, int _trainIdx, float _distance)
        You should set the queryIdx attribute to the index of the feature in the first image,
        the trainIdx attribute to the index of the feature in the second image and the distance attribute to the
        distance between the two features as defined by the particular distance metric (e.g., SSD or ratio).
        """
        raise NotImplementedError


class SSDFeatureMatcher(FeatureMatcher):

    def matchFeatures(self, descriptors_1: np.ndarray, descriptors_2: np.ndarray) -> List[cv2.DMatch]:
        # to collect
        matches: List[cv2.DMatch] = list()
        # first, we compute the sum-of-squares distance (pairwise).
        dist_mat = cdist(descriptors_1, descriptors_2, metric='euclidean')  # [k_1, d_1] , [k_2, d_2] -> [k_1, k_2].
        min_list = np.argmin(dist_mat, axis=1).tolist()  # along k_2. we want to find the closest descriptor to each k_1
        for k_1_idx, k_2_idx in enumerate(min_list):
            match = cv2.DMatch(_queryIdx=k_1_idx, _trainIdx=k_2_idx, _distance=dist_mat[k_1_idx, k_2_idx])
            matches.append(match)  # collect
        return matches


class RatioFeatureMatcher(FeatureMatcher):

    def matchFeatures(self, descriptors_1: np.ndarray, descriptors_2: np.ndarray) -> List[cv2.DMatch]:
        # to collect
        matches: List[cv2.DMatch] = list()
        # we still need the distance
        dist_mat = cdist(descriptors_1, descriptors_2, metric='euclidean')
        min_list = np.argmin(dist_mat, axis=1).tolist()
        for k_1_idx, k_2_idx in enumerate(min_list):
            min_dist = dist_mat[k_1_idx, k_2_idx]
            dist_mat[k_1_idx, k_2_idx] = np.inf  # just a ridiculously large num
            sec_min_dist = dist_mat[k_1_idx].min()
            ratio = min_dist / sec_min_dist
            match = cv2.DMatch(_queryIdx=k_1_idx, _trainIdx=k_2_idx, _distance=ratio)
            matches.append(match)
        return matches


# --- utils --- #
def load_vars() -> Tuple[List[str], List[np.ndarray]]:
    """
    this is for loading all the variation images
    """
    names = os.listdir(VARS_DIR)
    var_paths = [
        os.path.join(VARS_DIR, file_name)
        for file_name in names
    ]
    # load all of them in numpy arrays
    variations = [
        cv2.imread(var_path, cv2.IMREAD_GRAYSCALE)
        for var_path in var_paths
    ]

    return names, variations


# instantiate this here
orb = cv2.ORB_create()


def extract_kps(image: np.ndarray, mode: str, thresh: float) -> List[cv2.KeyPoint]:
    """
    extract this either with your implementation, or with orb's built-in function
    """
    global orb
    if mode == "harris":
        return harris_points_detector(image, thresh)
    elif mode == "orb":
        # find the keypoints with ORB
        return orb.detect(image, None)
    else:
        raise ValueError("Invalid mode:", mode)


def write_text(image: np.ndarray, text: str) -> np.ndarray:
    # Write some Text
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10, 10)
    fontScale = 10
    fontColor = (255, 255, 255)
    lineType = 2

    return cv2.putText(image, text,
                       bottomLeftCornerOfText,
                       font,
                       fontScale,
                       fontColor,
                       lineType)


def main():
    global orb
    # now... you might want to ... visualise all of that.
    parser = argparse.ArgumentParser()
    parser.add_argument("--kps_mode", type=str,
                        default="orb")
    parser.add_argument("--matcher_mode", type=str,
                        default="ssd")
    parser.add_argument("--thresh", type=float,
                        default=0.0009)

    # parse args
    args = parser.parse_args()
    kps_mode: str = args.kps_mode
    matcher_mode: str = args.matcher_mode
    thresh: float = args.thresh

    # --- prepare the matcher --- #
    if matcher_mode == "ssd":
        matcher = SSDFeatureMatcher()
    elif matcher_mode == "ratio":
        matcher = RatioFeatureMatcher()
    else:
        raise ValueError

    # --- load the images --- #
    bernie = cv2.imread(BERNIE_JPEG, cv2.IMREAD_GRAYSCALE)  # the original bernie image
    names, variations = load_vars()  # the variations of bernie
    # --- first extract the features of the bernie --- #
    bernie_kps = extract_kps(bernie, kps_mode, thresh)
    _, bernie_descriptors = orb.compute(bernie, bernie_kps)
    # --- now match that with the variations --- #
    for bernie_name, bernie_var in zip(names, variations):
        bernie_var_kps = extract_kps(bernie_var, kps_mode, thresh)
        _, bernie_var_descriptors = orb.compute(bernie_var, bernie_var_kps)
        # find the matches
        if bernie_var_descriptors is None:
            matches = list()
        else:
            matches = matcher.matchFeatures(bernie_descriptors, bernie_var_descriptors)
        # now, visualise the matches
        drawn = cv2.drawMatches(bernie,
                                bernie_kps,
                                bernie_var,
                                bernie_var_kps,
                                matches,
                                None,
                                matchColor=(0, 255, 0),  # those that have been matched are drawn green
                                singlePointColor=(255, 0, 0),  # those that have not been matched are drawn red
                                matchesMask=None   # all matches are drawn
                                )
        plt.imshow(drawn)
        plt.title(bernie_name)  # name it
        plt.show()


if __name__ == '__main__':
    main()
