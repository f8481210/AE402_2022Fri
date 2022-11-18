#匯入
import tkinter as tk

#創建視窗
root = tk.Tk()

#設定視窗標題
root.title('MENU')
#設定視窗大小
root.geometry('300x300')

#創建選單欄 menubar
menubar = tk.Menu(root)

#綁定選單
root.config(menu = menubar)
'''
#新增選單項目一 (父選單)
menubar.add_command(label = '新增檔案')

#新增選單項目二 (父選單)
menubar.add_command(label = '編輯')
'''
#創建子選單1 放在父選單裡面
menu1 = tk.Menu(menubar,tearoff = 0)
menu2 = tk.Menu(menubar)

#新增子選單項目
menu1.add_command(label = '打開檔案')
menu1.add_separator()
menu1.add_command(label = '關閉檔案')


#命名父選單，並綁定對應子選單
menubar.add_cascade(menu = menu1, label = '檔案')


#執行
root.mainloop()