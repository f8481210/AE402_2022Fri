import random
password = random.choice([139,193,319,391,913,931])
lefttime = 3
while lefttime > 0:             
    guess = int(input("Please enter a 3-digit password, %d time left:"%(lefttime))) 
    if guess != password:
        print('Incorrect password please try again')
        lefttime -= 1
    if guess == password:
        print('Welcome to login!')
        break
        pass
    pass
else:
 print('The account has been locked')
    
    
