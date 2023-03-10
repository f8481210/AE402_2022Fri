#抓取博客來暢銷排行榜前30名，並輸出名次、書名及售價。
#匯入模組
import requests
from bs4 import BeautifulSoup

#輸入網址
url = 'https://www.books.com.tw/web/sys_saletopb/books'

#發送請求
#請求成功 > 網頁程式碼
#請求失敗 > 404 ERROR
data = requests.get(url)

#解析html
#BeautifulSoup(解析內容, 解析器)
#解析器 > 'html.parser'
soup = BeautifulSoup(data.text,'html.parser')

#搜尋書名 div class='type02_bd-a' > h4 > a
#搜尋價格 div class='type02_bd-a' > ul > 
#         li class='price_a' > strong
booknames = soup.find_all("div",class_ = "type02_bd-a")

#名次
num = 1

#取出書名
for i in booknames:
    h4 = i.find('h4')
    ul = i.find('ul')
    if h4 and ul:
        a = h4.find('a') #書名
        li = i.find('li',class_ = 'price_a') #價格
        if a and li:
            strongs = li.find_all('strong')
            if len(strongs) == 2:
                print(num,a.text,strongs[1].text)
                num += 1
                if num > 30:
                    break