#匯入模組
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#宣告瀏覽器
c = webdriver.Chrome()

#到指定頁面
url = "https://www.google.com.tw/"
c.get(url)

time.sleep(0.5)

#搜尋輸入框
inputBar = c.find_element_by_tag_name('textarea.q')
inputBar.send_keys("youtube")

#利用Keys直接針對inputbar按下鍵盤Enter
inputBar.send_keys(Keys.Enter)

time.sleep(0.5)

#搜尋跟關鍵字符合的網頁
c.find_element_by_partial_link_text("Youtube").click()

time.sleep(0.5)

#截圖
c.save_screenshot('yt.png')

#關閉網頁
c.close()
