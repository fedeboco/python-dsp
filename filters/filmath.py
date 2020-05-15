def pi():
    return 3.14159265358979323846

def pow(x, n):
    p = 1
    for i in range(0, n):
        p = p * x   
    return p

def fact(x):
    f = 1
    while (x > 1):
        f = f * x
        x = x - 1
    return f

def sign(x):
    if (x < 0):
        return -1
    return 1

def abs(x):
    s = sign(x)
    return s * x

def sin(x):
    s = 0
    sgn = sign(x)
    x = abs(x)
    p = pi()
    while(x > 2 * p):
        x = x - 2 * p
    x = sgn * x
    for n in range(0, 30):
        s = s + pow(-1, n) * pow(x, 2 * n + 1) / fact(2 * n + 1)
    return s

def cos(x):
    s = 0
    sgn = sign(x)
    x = abs(x)
    p = pi()
    while(x > p):
        x = x - p
    x = sgn * x
    for n in range(0, 30):
        s = s + pow(-1, n) * pow(x, 2 * n) / fact(2 * n)
    return s