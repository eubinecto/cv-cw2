


image | thresh | kps
--- | --- | ---
![](.logs_images/27a1dd54.png) | max * 0.6 = 130288105450.56 | 62
![](.logs_images/0d854384.png) | max * 0.5 = 108573421208 | 151 
![](.logs_images/71a5c67b.png) | max * 0.4 = 86858736967 | 346
![](.logs_images/8a9254ae.png) | max * 0.3 = 65144052725 | 797
![](.logs_images/4cad465d.png) | max * 0.2 = 43429368483 | 2003
![](.logs_images/2c107595.png) | max * 0.1 = 21714684241| 5508


the number of key points decreases exponentially.
what is the best one? -> only leaving out the corners on the gloves would be much better. 


the optimal value is max * 0.5. Because it has the least off-the-bernie spots.
