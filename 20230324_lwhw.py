import re
str1 = 'its raining cats and dogs'
str2 = 'number:0912345678'
'''
print(re.search('\S',str1))
print(re.fullmatch('\D*',str1))
print(re.match('\w+',str2))
print(re.search('[^0-9]{8}',str2))
'''
string=re.sub("\d",'12',str2)
print(string)
print(len(re.findall('12', str2)))
print(len(re.findall('12',string)))

#^[A-Z]\d{9}$ #A123456789
#^\d{4}-\d{2}-\d{2}$ 0912-34-56