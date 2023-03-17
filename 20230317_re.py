import re

pattern1 = 'cat'
pattern2 = 'dog'

string = "in the house cat"
string2 = "cat in the house"
string3 = 'cat'
#print(pattern1 in string)
#print(pattern2 in string)
#print(re.search(pattern1, string)) #搜尋
#print(re.match(pattern1, string2)) #字首開始判斷
#print(re.fullmatch(pattern1, string3)) #一模一樣

#代替 sub(被替換的單字, 取代的單字 , 句子)
#print(re.sub(pattern1,pattern2,string))

string4 = 'cat in the house cat'
#print(re.findall(pattern1,string4))
#找到的結果存成list
'''
temp = '123w'
if re.fullmatch('[0-9]+',temp) != None:
    print(int(temp))
else:
    print('型態錯誤')    
'''
'''
temp2 = '23'

#num = 123
#num = '123'
#[0-9] = \d
print(re.fullmatch('\d+' , temp2))
'''

temp3 = '23'
print(re.fullmatch('\d\d' , temp3))
