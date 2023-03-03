html_sample = '''
<html>
<head>
<title>Story</title>
</head>
<body>
<a href="www.a.com" class="L" >A</a>
<p class="story">在很久以前，有一個國家叫猿創力</p>
<a href="www.b.com" class="I">B</a>
</body>
</html>'''

#匯入模組
from bs4 import BeautifulSoup
#解析
soup = BeautifulSoup(html_sample,'html.parser')

#印出
#print(soup.title)
#print(soup.p)
#print(soup.p.text)
#print(soup.a)
#print(soup.find_all('a'))
print(soup.find_all('a',class_ ='I'))