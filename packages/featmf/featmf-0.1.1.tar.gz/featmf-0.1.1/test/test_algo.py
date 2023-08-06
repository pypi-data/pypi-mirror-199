# Testing keypoint detection and description algorithms
"""
    Currently testing SIFT
"""

# %%
import os
import sys
from pathlib import Path
# Set the "./../src" from the script folder
dir_name = None
try:
    dir_name = os.path.dirname(os.path.realpath(__file__))
except NameError:
    print("WARNING: __file__ not found, trying local")
    dir_name = os.path.abspath('')
lib_path = os.path.realpath(f"{Path(dir_name).parent}/src")
# Add to path
if lib_path not in sys.path:
    print(f"Adding library path: {lib_path} to PYTHONPATH")
    sys.path.append(lib_path)
else:
    print(f"Library path {lib_path} already in PYTHONPATH")


# %%
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from typing import List
from PIL import Image
from featmf.utilities import kpts_cv2np
from featmf.lfdd import SIFT



# %%

# %%
sift = cv.SIFT_create()

# %%
# img_file = "/home2/avneesh.mishra/001.jpg"
img_file = "/scratch/avneesh.mishra/featmf/home.jpg"
img_cv = cv.imread(img_file)

# %%
img_gray = cv.cvtColor(img_cv, cv.COLOR_BGR2GRAY)


# %%
kp_cv, desc_cv = sift.detectAndCompute(img_gray, None)

# %%
kpts, scores = kpts_cv2np(kp_cv, True, True, True, True)

# %%
algo = SIFT(root_sift=True)

# %%
res = algo(img_gray)

# %%
assert np.allclose(res.keypoints, kpts), "Keypoints don't match"


# %%
i=123   # From: np.argsort([k.size for k in kp_cv])[-10:]
# kps_cv = kp_cv[i:i+1]
kps_cv = kp_cv
img_res = cv.drawKeypoints(img_gray, kps_cv, None, 
        flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
plt.imshow(img_res[..., ::-1])
plt.show()
print(f"Position: {kps_cv[0].pt}")
print(f"Angle: {kps_cv[0].angle:.2f}")
print(f"Size: {kps_cv[0].size:.2f}")

# %%
ang = np.deg2rad(kps_cv[0].angle)
r = round(kps_cv[0].size/2)
xb, yb = round(kps_cv[0].pt[0]), round(kps_cv[0].pt[1])
xe, ye = round(xb + r * np.cos(ang)), round(yb + r * np.sin(ang))
rimg = img_gray.copy()
rimg = np.repeat(rimg[..., None], 3, axis=2)
cv.circle(rimg, (xb, yb), r, (0, 0, 255), 1, cv.LINE_AA)
rimg = cv.line(rimg, (xb, yb), (xe, ye), (0, 0, 255), 1, cv.LINE_AA)
plt.imshow(rimg)
# plt.vlines([xb-r, xb+r], 0, rimg.shape[0])
# plt.hlines([yb-r, yb+r], 0, rimg.shape[1])
plt.show()

# %%
from featmf.utilities import draw_keypoints

# %%
rimg2 = draw_keypoints(img_gray, kpts, draw_angle=True)
plt.imshow(rimg2)
plt.show()

# %%
res2 = res.copy().sort_scores(1000)
rimg3 = draw_keypoints(img_gray, res2.keypoints, draw_angle=True)
plt.imshow(rimg3)
plt.show()

# %%


# %%
