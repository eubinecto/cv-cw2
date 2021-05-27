---
title: Computer Vision CW2 - Local Feature Detection and matching for object recognition
author: | 
  | Eu-Bin KIM
date: May 2021
output: pdf_document
geometry: margin=2cm
---


# Interest point (Keypoint) Detection

`harris_points_detector` is implemented at lines 17-70 in `identify_kps.py`.  Here,
reflective image padding is implemented by choosing `mode=reflect` whenever we call any `scipy`'s 
filter functions (i.e. `sobel`, `convolve` and `maximum_filter`). The horizontal &
vertical partial derivatives, `image_dx`  and `image_dy`, are calculated by convolving the input image with
a `sobel` filter. With this, we subsequently compute the components of the harris matrix: `Ixx`, `Iyy` and `Ixy`.
We then compute the corner response, `corner_mat`,  using a 7 by 7 `getGaussianKernel` of 0.5 sigma.

0.000001(12683) | 0.0001(2763) | **0.01(283)** - optimal
--- | --- | ---
![](../.logs_images/35c8c4bd.png){width=200px} | ![](../.logs_images/b12271ae.png){width=200px} | ![](../.logs_images/009de12b.png){width=200px}

Table: The detected keypoints with varying thresholds. The numbers in the parenthesis represent the total number of detected points.

![The number of detected keypoints with varying threshold. ](.report_images/627a4247.png){width=350px}


The strongest keypoints (i.e. interest points) are found by thresholding the local maxima of `corner_mat`.
As **Table 1** illustrates, we keep increasing the threshold until we have only a few off-the-bernie points. For instance,
we increase the threshold from `0.000001` all the way up to `0.01`, because many of 12683 keypoints in the former case
reside at the staircase, whereas we see only a few keypoints residing at the staircase in the latter case. As a result of this process,
we reach an optimal value of **0.01** for the threshold (the rightmost bernie in **Table 1**). Though possible, we do not further optimise 
from this value because the number of keypoints exponentially decreases as the threshold increases (**Figure 1**);
raising the threshold would only so much improve the result.

# Feature Matching


## Implement sum of squared distances to measure Local Feature similarity and ratio test to discard points that will give ambiguous matches 
- this is implemented at ... in `match_bernie.py`


## Calculate ORB Local features (using ORB descriptor) for your detected interest points.
- this is implemented at ... in `match_bernie.py`

## Compare it with built-in ORB features 
- we show the comparison below.
- some good: 
- some bad: the noisy ones.

harris corner detector | ORB's built-in `detect`
--- | ---
![](../.logs_images/f75eef27.png){width=300px} | ![](../.logs_images/cd9953a2.png){width=300px}
 ![](../.logs_images/0023038d.png){width=300px} | ![](../.logs_images/dd05ba3b.png){width=300px}
 ![](../.logs_images/76abf955.png){width=300px} | ![](../.logs_images/4b0fb639.png){width=300px} 
 ![](../.logs_images/7a7c5351.png){width=300px} |  ![](../.logs_images/2765a6ca.png){width=300px}
![](../.logs_images/c65430b4.png){width=300px} | ![](../.logs_images/e92a03a0.png){width=300px}
![](../.logs_images/dbd0c378.png){width=300px} |  ![](../.logs_images/1d7911c2.png){width=300px}
 ![](../.logs_images/6b7759e4.png){width=300px} |  ![](../.logs_images/5b45cd3b.png){width=300px}
![](../.logs_images/f6679664.png){width=300px} | ![](../.logs_images/87cc68ca.png){width=300px}
 ![](../.logs_images/9d8a512a.png){width=300px} | ![](../.logs_images/dba42e5d.png){width=300px}


