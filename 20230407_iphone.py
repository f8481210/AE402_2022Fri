#題目：取前100筆資料，顯示商品名稱和價錢。

#匯入模組
import requests

#一頁N筆資料
count = 0

pageNumber=1

#要100筆資料，一直執行的條件？
#先計算一頁有幾筆資料
while pageNumber <2:
    #format(要插入字串{}裡的值)
    
    data = requests.get("https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=iphone&page={}&sort=sale/dc".format(pageNumber))
    pageNumber += 1
    
    #json資料轉換成python格式
    data = data.json()['prods']
    
    for i in data:
        name = i['name']
        price = i['price']
        print(name,price)
        count += 1
        
print(count)