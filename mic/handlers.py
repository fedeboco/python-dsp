from numpy import array, zeros

# this class modifies handles values using callbacks,
# notifing to calling observers when modified

class Handlers:
    values = zeros(10)
    _callbacks = [] 

    def __init__(self, initialValue = 50):
        for n in range(len(self.values)):
            self.values[n] = initialValue 

    @property
    def value(self):
        return self.values

    def getValue(self, index):
        return self.values[index]

    @value.setter
    def value(self, value):
        self.values[value[0]] = value[1]
        self._notify_observers(value[0])

    def _notify_observers(self, handleNumber):
        for callback in self._callbacks:
            callback(handleNumber)

    def register_callback(self, callback):
        self._callbacks.append(callback)