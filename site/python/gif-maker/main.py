import glob
from PIL import Image
import cv2
import imageio
import random
import numpy as np
# filepaths
MAX_TRANSITIONS = 30
ALL_IMAGES = []

fp_in = "../../static/assets/img/me.jpg"
fp_out = "../../static/assets/img/processed.gif"
globs = list(reversed(sorted(glob.glob(fp_in))))
backSub = cv2.createBackgroundSubtractorMOG2()

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
# Sobel Edge Detection
for index, image_file in enumerate(globs):
  original_image  = cv2.imread(image_file)
  img_blur = cv2.GaussianBlur(original_image,(3,3), sigmaX=0, sigmaY=0)
  edges = [
    cv2.Canny(img_blur,50,200),
    cv2.Canny(img_blur,100,150),
    cv2.Canny(img_blur,150,100),
    cv2.Canny(img_blur,200,50)
  ]
  # colored_edges = []
  # for index, edge in enumerate(edges):
  #   img2 = original_image.copy()
  #   rgb = cv2.cvtColor(edge, cv2.COLOR_GRAY2RGB)
  #   rgb *= np.array((1,0,0),np.uint8) # set g and b to 0, leaves red :)
  #   colored_edges.append(np.bitwise_or(img2, rgb))
  
  for transition in range(MAX_TRANSITIONS):
    random.shuffle(edges)
    ALL_IMAGES.extend(edges)

with imageio.get_writer(fp_out, mode="I") as writer:
  for idx, frame in enumerate(ALL_IMAGES[0:60]):
        print("Adding frame to GIF file: ", idx + 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        writer.append_data(rgb_frame)