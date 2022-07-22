import random
answer = random.randint(1,100)
lefttime = 0
while lefttime<10:
    left = 10-lefttime              
    guess = int(input("請猜數字(1~100)，還剩%d次:"%(left)))
    if guess>answer:          
        print ('數字太大')
    elif guess<answer:
        print ('數字太小')
    else:
		print ('恭喜答對! ')
        break            
    lefttime += 1
if lefttime==10:              
    print ('遊戲結束，你沒猜到。答案是%d'%(answer))
    
    
    
