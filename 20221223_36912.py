import turtle
tur = turtle.Turtle()

#設置畫面大小
turtle.setup(650,650)

def number(num):
    tur.penup()
    tur.forward(200)
    tur.write(num)
    tur.back(200)
    tur.pendown()

number(3)
tur.right(90)
number(6)
tur.right(90)
number(9)
tur.right(90)
number(12)

#完成程式
turtle.done()
turtle.exitonclick()
