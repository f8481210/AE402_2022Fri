from pytube import YouTube

#Chunk 還沒寫入硬碟的資訊
#file_handle 正在寫入的資訊
#bytes_remaining還剩下多少bytes沒下載完
def showProgress(chunk, file_handle, bytes_remaining):
    #總檔案大小
    size = video.filesize
    
    #總大小減剩下的大小 = 已經下載的大小
    #目前下載進度(總大小-剩餘大小)除總大小 = 已下載百分比
    #全部大小 - 剩餘大小 = 已經下載多少 *100/總大小
    
    currentProgress = (size - bytes_remaining)*100 / size
    print("目前進度：" + str(currentProgress) + "%")

yt = YouTube("https://www.youtube.com/watch?v=O1LOx07FS3M&ab_channel=THESTARMAGAZINE"
             ,on_progress_callback = showProgress)

video = yt.streams.filter(res='720p').first()

video.download()
