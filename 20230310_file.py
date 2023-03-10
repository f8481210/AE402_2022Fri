# 寫入檔案 命名成test
file = open('test.txt','a+')

# a a+
# w w+

# 讀取檔案內容
temp = file.read()

# 印出內容
print(temp)

# 開始寫檔
file.write('0804')

# 關閉檔案
file.close()