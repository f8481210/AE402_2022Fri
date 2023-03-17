#抓取博客來暢銷排行榜前30名的照片並存入電腦。

#匯入模組
import requests
from bs4 import BeautifulSoup

#輸入網址
url = 'https://www.books.com.tw/web/sys_saletopb/books'

#發送請求
data = requests.get(url)

#解析
soup = BeautifulSoup(data.text,'html.parser')

#搜尋標籤 li > img
list1 = soup.find_all('li',class_ = 'item')

num = 1

#找到img標籤
for i in list1:
    img = i.find('img',class_="cover")
    if img:
        src = img['src'] #圖片網址
        alt = img['alt'] #圖片名稱 書名
        
        imgdata = requests.get(src)
        #print(imgdata)#確認圖片網址是否傳送成功
        #print(imgdata.content) #.content 顯示二進位的內容
        #print(alt,src)
        with open(alt+'.jpg' , 'wb') as f:
            f.write(imgdata.content)
        
        #自行修改成前30本書
        num += 1
        if num > 2:
            break
      