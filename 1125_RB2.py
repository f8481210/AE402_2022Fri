import tkinter as tk
window = tk.Tk()
window.title("Menu")
window.geometry("500x500")

def selection():
    label.config(text = '我選擇的是:' + string.get())

#宣告變數
string = tk.StringVar()

label = tk.Label(window,bg='#F00',text = '尚未選擇')
label.pack()

r1 = tk.Radiobutton(window,text = 'AAA',variable = string, 
                    value = 'A',command = selection)
r1.pack()

r2 = tk.Radiobutton(window,text = 'BBB',variable = string,
                    value = 'B',command = selection)
r2.pack()

#start
window.mainloop()