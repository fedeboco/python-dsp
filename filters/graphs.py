import matplotlib.pyplot as plt

def plot(vector, yAxisLabel = "y [n]"):
    plt.figure()
    plt.stem(vector, basefmt = " ", use_line_collection = True)
    plt.show(block=False)
    plt.grid()
    plt.xlabel('n')
    plt.ylabel(yAxisLabel)

def closeAll():
    input("q to quit.\n")
    plt.close('all')