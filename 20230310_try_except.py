# 檔案錯誤處理
file = open('0310.txt','r')

#先嘗試 > 可執行
try:
    file.read()
    
#先嘗試 > 不能執行
except:
    print('ERROR')
    
#不管能不能執行
finally:
    file.close()