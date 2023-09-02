# TODO
from cs50 import get_float

# cdtaking the input
n = -1
while (n < 0):
    n = get_float("Change owed: ")

# geting value of summ
summ = 0
n *= 100
g = int(n)
X = [25, 10, 5, 1]

for i in X:
    summ += int(g / i)
    g %= i

print(summ)