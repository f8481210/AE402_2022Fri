# 台鐵查詢台北到台中，2023/03/31的所有車次時間

#匯入模組
import requests
from bs4 import BeautifulSoup

#我要傳遞的資料
data = {
            "startStation": "1000-臺北",
            "endStation": "3300-臺中",
            "transfer": "ONE",
            "rideDate": "2023/03/31",
            "startOrEndTime": "true",
            "startTime": "00:00",
            "endTime": "23:59",
            "trainTypeList": "ALL"}

#網址Request URL
res = requests.post("https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybytime",data = data)
#print(res)

#解析
soup = BeautifulSoup(res.text,"html.parser")

#印前10資料
for i in range(10):
    time = soup.find_all('',class_="train-number")[i]
    trainNumber = soup.find_all('ul',class_="train-number")[i]
    if trainNumber:
        for each_a in trainNumber:
            a = each_a.find('a')
            if a:
                print("車次",a.text)

