#匯入模組
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

#宣告瀏覽器
c = webdriver.Chrome()

#到指定頁面
url = "https://www.google.com.tw/"
c.get(url)

time.sleep(0.5)

#搜尋輸入框
inputBar = c.find_element(By.TAG_NAME , 'textarea') 
inputBar.send_keys("youtube")

#利用Keys直接針對inputbar按下鍵盤Enter
inputBar.send_keys(Keys.ENTER)

time.sleep(0.5)

#搜尋跟連結符合的文字
#https://www.youtube.com/?gl=TW&hl=zh-tw
c.find_element(By.PARTIAL_LINK_TEXT , "youtube").click()

time.sleep(0.5)

#截圖
c.save_screenshot('yt.png')

#關閉網頁
c.close()

















