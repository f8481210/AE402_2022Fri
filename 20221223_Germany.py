#德國國旗
#黑紅黃

import turtle
tur = turtle.Turtle()

#設置畫面大小
turtle.setup(650,650)

#定義畫矩形
def rectangle():
    tur.begin_fill()
    tur.forward(600)
    tur.right(90)
    tur.forward(200)
    tur.right(90)
    tur.forward(600)
    tur.right(90)
    tur.forward(200)
    tur.right(90)
    tur.end_fill()

#黑色
tur.penup()
tur.goto(-300,300)
tur.pendown()
tur.fillcolor('#000000')
rectangle()

#紅色
tur.penup()
tur.goto(-300,100)
tur.pendown()
tur.fillcolor('#FF0000')
rectangle()

#黃色
tur.penup()
tur.goto(-300,-100)
tur.pendown()
tur.fillcolor('#FFFF00')
rectangle()