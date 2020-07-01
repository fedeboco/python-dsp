# This module serves for performance testings purposes

pi = 3.14159265358979323846

# returns f(x) = x ^ n
# x is a scalar
def pow(x, n):
    p = 1
    for _ in range(0, n):
        p = p * x   
    return p

# returns f(x) = x!
# x is a scalar
def fact(x):
    f = 1
    while (x > 1):
        f = f * x
        x = x - 1
    return f

# returns -1 if x is negative or 1 otherwise
# x is a scalar
def sign(x):
    return 1 - 2 * (x < 0)

# returns f(x) = |x|
# x is a scalar
def abs(x):
    return x * sign(x)

# returns f(x) = sin(x)
# x is a scalar
def sin(x):
    s = 0
    sgn = sign(x)
    p = 2 * pi
    while( sgn * x > p ):
        x = x - sgn * p
    for n in range(0, 30):
        s = s + pow(-1, n) * pow(x, 2 * n + 1) / fact(2 * n + 1)
    return s

# returns f(x) = cos(x)
# x is a scalar
def cos(x):
    s = 0
    sgn = sign(x)
    x = abs(x)
    p = pi
    while(x > 2 * p):
        x = x - 2 * p
    x = sgn * x
    for n in range(0, 30):
        s = s + pow(-1, n) * pow(x, 2 * n) / fact(2 * n)
    return s

# returns f(x) = sinc(x) = sin(x) / x
# x is a vector or scalar
def sinc(x):
    s = []
    for i in range(0, len(x)):
        val = x[i]
        if (val != 0):
            s.append(sin(val) / val)
        else:
            s.append(1)
    return s