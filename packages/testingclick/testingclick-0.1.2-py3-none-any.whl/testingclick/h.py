
#a = 5
#b = 7

def s(m, n):
    global a, b
    a = m
    b = n
    return a + b

print(s(2, 3))
print(a)
print(b)
