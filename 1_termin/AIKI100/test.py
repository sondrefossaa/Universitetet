import random as r

n = 10
a = [0,1,2,3,4,5,6,7,8,9]
b = 0
for i in range(n):
    b = b + r.randint(0, 10000)
    print(b)
