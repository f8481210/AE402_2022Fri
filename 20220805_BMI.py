Height = float(input("請輸入身高(cm):"))/100
Weight = float(input("請輸入體重(kg):"))
BMI = round(Weight/(Height**2),1)
if BMI<18.5:
    note = '你太輕囉！'
elif BMI>=18.5 and BMI<24:
    note = '你的體重正常！'
elif BMI>=24 and BMI<27:
    note = '你現在過重了喔!'
elif BMI>=27 and BMI<30:
    note = '你現在輕度肥胖了喔!'
elif BMI>=30 and BMI<35:
    note = '你現在中度肥胖了喔!'
else:
    note = '你現在重度肥胖了喔!'
print('你的 BMI 數值為：{0}，{1}'.format(BMI, note))
