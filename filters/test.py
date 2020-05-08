import numpy as np
import windows
import graphs

rect1 = windows.rectangular(5, 2, 10)
rect2 = 2 * windows.rectangular(7, 2, 10)
bart1 = windows.bartlett(12, 3, 24)
graphs.plot(rect1 - rect2, "w [n]")
graphs.plot(bart1)
graphs.closeAll()