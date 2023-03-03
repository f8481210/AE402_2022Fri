#匯入requests模組
import requests

#輸入網址
url = 'http://www.youtube.com'

#發送請求
data = requests.get(url)

#印出結果
print(data)

#印出程式碼
print(data.text)