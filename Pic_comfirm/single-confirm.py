import cv2

# 采用灰度值的原因，图片是静态的，对于光照和亮度的依赖不大
base = cv2.imread('base.jpg', 0)
aim = cv2.imread('aim.jpg', 0)

h, w = aim.shape[:2]

# 匹配函数的返回值是幅图灰度图像，在这幅图中最白的地方表示最大的匹配
# templateMatchModes
res = cv2.matchTemplate(base, aim, cv2.TM_CCOEFF_NORMED)

# 获取这幅图中最小值和最大值，以及他们对应的坐标
# 这里我们只用到了最大匹配的坐标
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

print(max_loc, max_val)
left_top = max_loc
right_bottom = (left_top[0]+w, left_top[1]+h)

# 通过确定对角线画矩形,2代表划线的宽度
cv2.rectangle(base, left_top, right_bottom, 255, 2)
cv2.imshow("processed", base)

# 0 is the special value that means "forever"
cv2.waitKey(0)
