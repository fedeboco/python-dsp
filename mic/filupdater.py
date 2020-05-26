from multiprocessing import Queue
from filters.settings import guiSettings

class filterUpdater():
    queue = Queue()
    guiSettings = guiSettings()

    def __init__(self, queue):
        self.queue = queue

    def getQueue(self):
        return self.queue

    def update(self):
        while ( True ):
            self.guiSettings = self.queue.get()
            if ( self.guiSettings == None ):
                break
            self.guiSettings.printSettings()
            print("received.")
