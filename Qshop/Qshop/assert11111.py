assert 3>1,'第一个值不大于第二个值'

age=input(">>>")

assert age.isdigit(),"%s不是数字"%age

print(int(age))