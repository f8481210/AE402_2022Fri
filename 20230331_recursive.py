# 1 ~ 100 總和

#for迴圈
num = 0
for i in range(1,101):
    num += i
    #num = num + i
print('for:',num)

#while迴圈
ans = 0
count = 1
while count <= 100:
    ans += count
    #ans = ans + count
    count += 1
print('while:',ans)

#遞迴
def recursive(n):
    #終止條件
    if n<0:
        return 0
    return n + recursive(n-1)

print(recursive(100))