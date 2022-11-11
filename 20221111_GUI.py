# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 18:23:22 2022

@author: N
"""
#匯入tkinter
import tkinter as tk
import tkinter.messagebox

def click():
    tkinter.messagebox.showinfo(title='提示',message='幹嘛點我')

#宣告/創建視窗
window = tk.Tk()

#設定標題
window.title("I'm XXX")

#設定視窗大小
window.geometry('500x300')

#label元件
label = tk.Label(window,text = 'Hello!!!',bg ='#000000',fg='#FFFFFF')
label.pack()

#Entry元件
entry = tk.Entry(window, width = 30)
entry.pack()

#Button元件
button = tk.Button(window, text='Button',bg = '#FFDC35',command = click)
button.pack()

#執行視窗
window.mainloop()

