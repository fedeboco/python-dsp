import matplotlib.pyplot as plt

def plot(vector, yAxisLabel = "y"):
    plt.figure()
    #plt.stem(vector, basefmt = " ", use_line_collection = True)
    plt.plot(vector)
    plt.show(block=False)
    plt.grid()
    plt.xlabel('n')
    plt.ylabel(yAxisLabel + " [n]")
    plt.title(yAxisLabel)

def closeAll():
    input("q to quit.\n")
    plt.close('all')

def multiPlot(vectors, rows = 1, cols = 1, legends= []):
    plotted = 0
    legendsPlotted = 0
    L = len(vectors)
    P = len(legends)
    fig, axs = plt.subplots(rows, cols)
    for row in range(0, rows):
        for col in range(0, cols):
            if (plotted < L):
                axs[row, col].stem(vectors[plotted], basefmt = " ", use_line_collection = True)
                axs[row, col].grid()
                axs[row, col].set_xlabel('n')
                axs[row, col].set_ylabel('y [n]')
                plotted = plotted + 1
                if (legendsPlotted < P):
                    axs[row, col].legend(legends[legendsPlotted])
    fig.show()
