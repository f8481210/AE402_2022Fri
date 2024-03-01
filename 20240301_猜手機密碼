import random

def reset():
    password = random.choice([139, 193, 319, 391, 913, 931]) # 重新亂數
    lefttime = 3 # 次數重製
    return password, lefttime
    
if __name__ == '__main__':
    password = random.choice([139, 193, 319, 391, 913, 931])
    lefttime = 3
    
    while lefttime > 0:
        guess = int(input("請輸入3位數的密碼，還剩%d次:"%(lefttime)))
        
        if guess == password:
            print('歡迎登入!')
            break
        else:
            lefttime -= 1
            if lefttime == 0:
                print('該帳戶已被鎖定')
                retry = int(input("輸入1重新開始，0結束:"))
                if retry == 1:
                    password, lefttime = reset()
                    print('重新開始，密碼已更新!')
                else:
                    print('結束')
            else:
                print('密碼錯誤請再試一次')
