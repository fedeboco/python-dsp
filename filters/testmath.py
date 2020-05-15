import filmath as fi
import numpy as np

accuracy = "{0:15.10f}"

for x in np.linspace(0, 10 * fi.pi()):
    a = fi.sin(x)
    b = np.sin(x)
    error = abs(a - b) / b * 100
    print(  accuracy.format(x), "  ",  
            accuracy.format(fi.sin(x)), " ", 
            accuracy.format(np.sin(x)), " ", 
            accuracy.format(error), "%")
