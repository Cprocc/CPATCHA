from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# 访问一个浏览器界面
browser = webdriver.Chrome('../drivers/chromedriver.exe')
browser.get('http://www.baidu.com/')


# 向浏览器提交我们的关键字
kw = browser.find_element_by_id("kw")
kw.send_keys("selenium", Keys.RETURN)

# 截屏
time.sleep(1)
browser.save_screenshot("temp.png")
