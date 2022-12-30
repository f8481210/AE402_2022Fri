#匯入模組
import turtle,time,datetime

#宣告第一隻烏龜
tur = turtle.Turtle()
#改變烏龜速度
tur.speed(10)

#1. 時鐘刻度
#左轉60度 (烏龜指向1)
tur.left(60)
for i in range(1,13): #(起點,終點+1)
    tur.penup()
    tur.forward(200)
    tur.write(i)
    tur.back(200)
    tur.pendown()
    tur.right(30)
    
#2. 時針分針秒針
#控制時針分針是否要更新
update = True
#控制秒針是否要更新
updateSecond = True

while True:
    #取得現在時間(24小時制)
    now = datetime.datetime.now()
    #轉換成12進制
    h = now.hour % 12
    m = now.minute
    s = now.second
    
    #if update == True:
    if update:
        #畫時針
        hour = turtle.Turtle()
        hour.color('#FF0000')
        #指針朝上
        hour.left(90)
        #一圈12小時(1小時向右轉30度)
        #分鐘也會影響到時針，一小時30度(每一分鐘 時針 向右轉0.5度)
        hour.right(h*30+m*0.5)
        hour.forward(120)
    
        #畫分針
        minute = turtle.Turtle()
        minute.color('#00FF00')
        minute.left(90)
        #360/60 = 6(每一分鐘 分針 向右轉6度)
        minute.right(m*6)
        minute.forward(150)
        
        #時針分針更新完畢
        update = False
    
    if updateSecond:
        #畫秒針
        second = turtle.Turtle()
        second.color('#FF8800')
        second.left(90)
        #6度/秒
        second.right(s*6)
        second.forward(180)
        
        #秒針更新完畢
        updateSecond = False

    #3. 讓秒針一直轉，指針會依據現在時間移動到正確位置  
    time.sleep(1) #讓程式睡一秒
    now = datetime.datetime.now()
    #取得新的分鐘
    mnew = now.minute
    #比較現在是不是同一個時間
    if mnew != m:
        update = True
        #清除
        hour.clear()
        minute.clear()
        #重畫
        hour.reset()
        minute.reset()
    
    updateSecond = True
    second.clear()
    second.reset()

turtle.done()
turtle.exitonclick()