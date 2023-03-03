#匯入模組
import requests
from bs4 import BeautifulSoup

#輸入網址
url = 'https://www.books.com.tw/web/sys_saletopb/books'
#發送請求
data = requests.get(url)
#解析
soup = BeautifulSoup(data.text,'html.parser')
#搜尋 div > h4 > a
list1 = soup.find_all("div",class_ = "type02_bd-a")

num = 1
#取出書名
for i in list1:
    h4 = i.find('h4')
    if h4:
        a = h4.find('a')
        if a:
            print('第'+str(num)+'名',a.text)
            num += 1