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

url = 'http://dun.163.com/trial/sense'
driver = webdriver.Chrome('./drivers/chromedriver.exe')
wait = WebDriverWait(driver, 20)
driver.get(url)
time.sleep(3)
driver.find_elements_by_xpath('//div[@class = "yidun_intelli-icon"]')[0].click()
