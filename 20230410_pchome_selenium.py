#題目：利用selenium，取得商品名稱。

#匯入模組
from selenium import webdriver
import time
from bs4 import BeautifulSoup

#宣告瀏覽器
c = webdriver.Chrome()

#前往頁面 > 搜尋ice cream商品
url ="https://ecshweb.pchome.com.tw/search/v3.3/?q=ice%20cream"
c.get(url)

#網頁會延遲一下 確保資料有載入 > 程式睡1秒
time.sleep(2)

#讓游標往下移
for i in range(3):
    c.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    time.sleep(1)
    
#page_source 讀取網頁原始碼
soup = BeautifulSoup(c.page_source, "html.parser")

#取得商品名稱
for i in soup.find_all("h5",class_="prod_name"):
    if i:
        name = i.text
        print(name)

#關閉網頁
c.close()
    
    
    
