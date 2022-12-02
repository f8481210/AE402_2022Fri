#匯入pytube模組內的YouTube
from pytube import YouTube
#匯入tkinter模組
import tkinter as tk

#定義全域變數，儲存目前下載進度
progress =0
#定義進度條函式 showProgress
def showProgress(stream,chunk,bytes_remaining):
    size = stream.filesize
    
    global progress
    #目前下載進度 progress
    #前一次的下載進度preprogess
    preprogress = progress
    
    #總大小減剩下的大小 = 已經下載的大小
    #目前下載進度(總大小-剩餘大小)除總大小 = 已下載百分比
    #全部大小 - 剩餘大小 = 已經下載多少 *100//總大小
    current = (size - bytes_remaining)*100 // size
    progress = current
    
    if preprogress != progress: #還在下載
        scale.set(progress)
        window.update()
        print("目前進度： " + str(progress) + "%")
    
    if progress == 100:
        print("下載完成")


#定義點擊下載按鈕的函式 onClick
def onClick():
    global var  #定義全域變數var，設定成entry中的文字內容
    var.set(entry.get())
    
    #例外處理，如果取得網址及下載錯誤，則發生例外
    try:
        yt = YouTube(var.get(),on_progress_callback=showProgress)
        stream = yt.streams.first()
        stream.download()
    except:
        print('下載失敗')

"""建立基本視窗"""
window = tk.Tk()
window.title("YouTube下載器")
window.geometry("500x150")
window.resizable(False,False)

#創建label元件
label = tk.Label(window,text = "請輸入YouTube影片網址")
label.pack()

#建立var變數來存取entry的內容
var = tk.StringVar()

#創建entry元件
entry = tk.Entry(window, width = 50)
entry.pack()

#創建button元件
button = tk.Button(window, text = "下載",command = onClick)
button.pack()

#創建scale元件
scale = tk.Scale(window, label='進度條',orient=tk.HORIZONTAL,
                 length=200, from_ = 0 , to = 100,
                 showvalue = True , tickinterval = 0)
scale.pack()

#開始運行視窗程式
window.mainloop()