from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import cv2
import numpy as np
from io import BytesIO
import time
import requests
import random


class CrackSlider(object):
    """
    通过浏览器截图，识别验证码中缺口位置，获取需要滑动距离，并模仿人类行为破解滑动验证码
    """

    def __init__(self):
        """
        url: 网站目标
        driver: 加载的selenium包含的chrome驱动
        wait：设置等待超时时间和等待时间，WebDriverWait(driver, timeout, poll_frequency=0.5, ignored_exceptions=None)
        zoom: 缩放系数
        """
        self.url = 'http://dun.163.com/trial/jigsaw'
        self.driver = webdriver.Chrome('./drivers/chromedriver.exe')
        self.wait = WebDriverWait(self.driver, 20)
        self.zoom = 1

    def open(self):
        """
        打开指定的网页
        """
        self.driver.get(self.url)

    def get_pic(self):
        """
        保存验证码图片
        """
        time.sleep(5)
        # until:等待加载出指定的元素再进行下一步
        # target:审查元素得到的验证图片信息
        # template:审查元素得到的小滑块图片信息
        target = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_bg-img')))
        template = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_jigsaw')))
        # 获取图片的链接
        target_link = target.get_attribute('src')
        template_link = template.get_attribute('src')
        # 将图片保存在本地
        target_img = Image.open(BytesIO(requests.get(target_link).content))
        template_img = Image.open(BytesIO(requests.get(template_link).content))
        target_img.save('target.jpg')
        template_img.save('template.png')

        # 对图片进行缩放，网页上的原版图片是320像素，和保存在本地之后的图像大小进行除法，得到缩放系数
        local_img = Image.open('target.jpg')
        size_loc = local_img.size
        self.zoom = 320 / int(size_loc[0])

    def get_tracks(self, distance):
        """
        模拟滑动轨迹
        """
        print(distance)
        # 移动的总距离增加20像素，我们会在移动过程中增加20像素的随机回退
        # distance += 20
        forward_tracks = []
        # current = 0
        # # mid 设置减速阈值，加速滑动到减速滑动
        # mid = distance * 3 / 4
        # t = random.randint(2, 3) / 5
        # v = 0
        # while current < distance:
        #     if current < mid:
        #         a = 2
        #     else:
        #         a = -3
        #     v0 = v
        #     v = v0 + a * t
        #     move = v0 * t + 1 / 2 * a * t * t
        #     current += move
        #     # 保留整数部分的move
        #     forward_tracks.append(round(move))

        forward_tracks.append(distance)
        # 设置随机的回退
        # back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -2]
        back_tracks = []
        return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}

    @staticmethod
    def match(target, template):
        """
        识别图片应该移动的位置
        """

        img_rgb = cv2.imread(target)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template, 0)
        w, h = template.shape[::-1]
        print(w, h)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        run = 1

        # 使用二分法查找阈值的精确值
        # 阈值在0,1 之间。得到满足于只得结果
        # 如果得到的结果数量大于1个，那么代表阈值的下限太小了增大L
        # 如果得到的结果只0个，那么代表阈值的上限太大了，缩小一下
        L = 0
        R = 1
        while run < 20:
            run += 1
            threshold = (R + L) / 2
            print(threshold)
            if threshold < 0:
                print('Error')
                return None
            loc = np.where(res >= threshold)
            print(len(loc[1]))
            if len(loc[1]) > 1:
                L += (R - L) / 2
            elif len(loc[1]) == 1:
                print('目标区域起点x坐标为：%d' % loc[1][0])
                break
            elif len(loc[1]) < 1:
                R -= (R - L) / 2
        return loc[1][0]

    def crack_slider(self):
        """
        拖动鼠标进行滑动
        """
        # 等待模块的出现
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'yidun_slider')))
        ActionChains(self.driver).click_and_hold(slider).perform()

        # 按照坐标的位置拖动
        for track in tracks['forward_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()

        time.sleep(0.5)
        for back_tracks in tracks['back_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=back_tracks, yoffset=0).perform()

        ActionChains(self.driver).move_by_offset(xoffset=0, yoffset=0).perform()
        ActionChains(self.driver).move_by_offset(xoffset=0, yoffset=0).perform()
        time.sleep(0.5)

        ActionChains(self.driver).release().perform()


if __name__ == '__main__':
    cs = CrackSlider()
    cs.open()
    target = 'target.jpg'
    template = 'template.png'
    cs.get_pic()
    distance = cs.match(target, template)
    tracks = cs.get_tracks((distance+8) * cs.zoom)
    cs.crack_slider()
    # cs.driver_close()

