# this file serves speed testing purposes

from filters import filmath as fi
from filters import graphs
import numpy as np

accuracy = "{0:15.10f}"
text = "{0:^15}"

print(  "   ",
        text.format("x"), 
        text.format("mine"), 
        text.format("numpy"), 
        text.format("error")    )

for x in np.linspace(0, 10 * fi.pi):
    a = fi.cos(x)
    b = np.cos(x)
    error = abs(a - b) / b * 100
    print(  accuracy.format(x),  
            accuracy.format(a), 
            accuracy.format(b),
            accuracy.format(error), "%")

lim = 8 * fi.pi
x = np.linspace(-lim, lim, 2500)
r = fi.sinc(x)
graphs.plot(r)
graphs.closeAll()