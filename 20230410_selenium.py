#selenium 自動化瀏覽器
#寫好程式 > 執行 > 自己打開瀏覽器 > pchome > 搜尋iphone

#匯入模組
from selenium import webdriver

#宣告瀏覽器
c = webdriver.Chrome()

#連接到指定網頁
url = "https://www.youtube.com/"
c.get(url)

#取得目前網址
temp = c.current_url()

#讀取網頁原始碼(html)
data = c.page_source()

#關閉瀏覽器
c.close()

#關閉瀏覽器且退出程式
c.quit()