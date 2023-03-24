import json
data = {
        #key : value
        'Name':'NN',
        'Height' : 164,
        "Male" : False                
        }
'''
#python to JSON
toJson = json.dumps(data)
print(type(data))

#print(toJson)
print(type(toJson))

# Json to python
toPython = json.loads(toJson)
print(toPython)
print(type(toPython))
'''
'''
#python 寫進 json
with open ('0734.json','w') as file:
    json.dump(data,file)

#讀取 json 轉成python
with open('0734.json','r') as file:
    read = json.load(file)
    print(read)
    print(type(read))
    print(read['Name'])
    print(type(read['Name']))
    '''
#課堂練習
data = {
        "name" : "your name" , 
        "birth" : 1120324 , #你的出生年月日 
        "Male" : False , #生理性別
        "position" : [30.5 , 3.0825 ,-500.0]
        }

# 1. 把上述資料轉成json檔案(寫檔)
with open ('2006.json' , 'w') as file:
    json.dump(data,file)
# 2. 讀取json檔案 轉成python資料
with open ('2006.json' , 'r') as file:
    read = json.load(file)
# 3. 印出 轉成python資料 的內容
    print(read)
# 4. 印出 轉成python資料裡的position
    print(read['position'])
