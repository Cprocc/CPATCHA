import cv2
import numpy as np

img_rgb = cv2.imread('mix-base1.jpg')
cv2.imshow('base', img_rgb)
cv2.waitKey(0)

img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('mix-aim1.jpg', 0)

h, w = template.shape[:2]

res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.9

loc = np.where(res >= threshold)
print(loc)

for pic in zip(*loc[::-1]):
    right_bottom = (pic[0] + w, pic[1] + h)
    cv2.rectangle(img_rgb, pic, right_bottom, 255, 1)

cv2.imshow('processed', img_rgb)
cv2.waitKey(0)
