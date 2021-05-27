
## Harris Corner detection

image | thresh | kps
--- | --- | ---
![](.logs_images/ed5ab0c1.png) | 0.1 | 12
![](.logs_images/009de12b.png) | 0.01 | 283
![](.logs_images/a62272ab.png) | 0.001 | 1169
![](.logs_images/b12271ae.png) | 0.0001 | 2763
![](.logs_images/175b00bf.png) | 0.00001 | 6195
![](.logs_images/35c8c4bd.png) | 0.000001 | 12683



the plot:
![](.logs_images/42a706a1.png)
- x: threshold
- y: number of kps.
- exponential drop.


## Feature Matching

### with harris corner

ssd | ratio
--- | --- 
![](.logs_images/810530a3.png) |![](.logs_images/f75eef27.png) 
![](.logs_images/9bd44f15.png) | ![](.logs_images/0023038d.png)
![](.logs_images/59e0a250.png) | ![](.logs_images/76abf955.png)
![](.logs_images/607b2d59.png) | ![](.logs_images/7a7c5351.png)
![](.logs_images/d66437a5.png) |![](.logs_images/c65430b4.png)
![](.logs_images/cffe1d92.png) |![](.logs_images/dbd0c378.png)
![](.logs_images/0e980062.png) | ![](.logs_images/6b7759e4.png)
![](.logs_images/fcf9feb6.png) |![](.logs_images/f6679664.png)
![](.logs_images/d6eb7696.png) | ![](.logs_images/9d8a512a.png)


you might also want to find out the differences in the number of matches...

### with orb


ssd | ratio
--- | ---
![](.logs_images/7b2540ce.png) | ![](.logs_images/cd9953a2.png)
![](.logs_images/70efa83c.png) | ![](.logs_images/dd05ba3b.png)
![](.logs_images/3b0762f5.png) | ![](.logs_images/4b0fb639.png) 
![](.logs_images/cf8196b2.png) | ![](.logs_images/2765a6ca.png)
![](.logs_images/693c9934.png) | ![](.logs_images/e92a03a0.png)
![](.logs_images/88cdca1f.png) | ![](.logs_images/1d7911c2.png)
![](.logs_images/628e6c6d.png) | ![](.logs_images/5b45cd3b.png)
![](.logs_images/15635b4b.png) | ![](.logs_images/87cc68ca.png)
![](.logs_images/67047781.png) | ![](.logs_images/dba42e5d.png)