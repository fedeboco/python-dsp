import matplotlib.pyplot as plt
import time

# plots signal
def plot(vector, yAxisLabel = "y"):
    fig = plt.figure()
    plt.plot(vector)
    plt.show(block=False)
    plt.grid()
    plt.xlabel('n')
    plt.ylabel(yAxisLabel + " [n]")
    plt.title(yAxisLabel)
    ax = plt.gca()
    ax.relim()
    ax.autoscale_view(True,True,True) # for multiprocessing
    fig.canvas.draw()

# plots frequency response of filter
def plotFilterResponse(vector, rate, yAxisLabel = "fft(x[n])"):
    L = int(len(vector) / 2)
    x = [n * rate / L / 1000 for n in range(L)]
    fig = plt.figure()
    plt.plot(x, vector[:L], 'ko--', linewidth=1, markersize=2, )
    plt.show(block=False)
    plt.grid()
    plt.xlabel('f [kHz]')
    plt.ylabel(yAxisLabel + " (f)")
    plt.title(yAxisLabel)
    ax = plt.gca()
    ax.relim()
    ax.autoscale_view(True,True,True) # for multiprocessing
    fig.canvas.draw()

# waits to signal for closing all graphs
def closeAll(quitRequested):
    while (not quitRequested.value):
        time.sleep(1)
    plt.close('all')

# opens multiple plots
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
