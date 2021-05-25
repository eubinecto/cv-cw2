import cv2
from tqdm import tqdm

from cv_cw2.paths import BERNIE_JPEG
import numpy as np


def main():
    bernie: np.array = cv2.imread(BERNIE_JPEG, cv2.IMREAD_GRAYSCALE)
    corner_mat = np.zeros(shape=bernie.shape)
    for x_idx in tqdm(range(corner_mat.shape[0])):
        for y_idx in range(corner_mat.shape[1]):
            pass


if __name__ == '__main__':
    main()