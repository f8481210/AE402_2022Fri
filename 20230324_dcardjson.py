#使用Dcard提供的API取得寵物版熱門文章前40篇的貼文
#讀取 標題 id topics 寫入一個新的json檔

# 1. 匯入模組
import json
import requests

# 2. 取得API內容
url = "https://www.dcard.tw/service/api/v2/forums/pet/posts?popular=true&limit=40"
#limit 會有幾篇貼文
respond = requests.get(url)

# 3. json to python
data = json.loads(respond.text)

# 4. 印出所需資料
for i in data:
    d = {
        'Title' : i['title'],
        'ID' : i['id'],
        'Topics' : i['topics']        
        }
    
    # 5. 寫入檔案 a模式才不會覆蓋掉前面資料
    with open('dcard_pet40.json','a' , encodinig = "utf-8") as file:
        json.dump(d,file,ensure_ascii = False)