#匯入模組
import turtle

#創建第一隻烏龜 / 畫筆
t1 = turtle.Turtle()

#創建畫布
screen = turtle.Screen()

#設定畫布 寬,高
screen.setup(800,600)

#舉起筆
t1.penup()
#移動
t1.goto(-300,200)
#放下筆
t1.pendown()

#設定顏色 色碼表
t1.fillcolor('#9F4D95')
#開始上色
t1.begin_fill()
#for 計數迴圈 
for i in range(4):
    t1.forward(100)
    t1.right(90)

#結束上色
t1.end_fill()

#完成
turtle.done()
#結束
turtle.exitonclick()