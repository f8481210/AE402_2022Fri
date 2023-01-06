import tkinter as tk

#宣告視窗
window = tk.Tk()
#設定視窗大小
window.geometry('300x300')

'''
#pack
tk.Label(window , text = 'top').pack(side="top")
tk.Label(window , text = 'bottom').pack(side = "bottom")
tk.Label(window , text='left').pack(side="left")
tk.Label(window , text='right').pack(side="right")
'''
'''
#grid 棋盤 
for i in range(1,10):
    for j in range(1,10):
        temp = tk.Label(window,text = i*j)
        temp.grid(row = i , column = j , padx = 5 ,pady = 5)
'''
#place 地方
tk.Label(window,text='place1').place(x=0 , y=0)
tk.Label(window,text='place2').place(x=150 , y =150)





#執行
window.mainloop()