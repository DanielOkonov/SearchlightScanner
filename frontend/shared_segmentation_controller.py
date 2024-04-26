class SharedSegmentation:
    def __init__(self):
        self._options = {
            1: None,
            4: (2, 2),
            9: (3, 3),
            16: (4, 4),
            25: (5, 5),
            32: (4, 8),
            40: (5, 8),
            50: (5, 10),
            60: (6, 10),
            84: (7, 12),
        }
        self._current = self._options[1]
        self._observers = []

    def register_observer(self, observer_callback):
        self._observers.append(observer_callback)

    def notify_observers(self):
        for callback in self._observers:
            callback(self._options)

    def get_options(self):
        return self._options
    
    def get_current(self):
        return self._current

    def set_current(self, new_value):
        print('SharedSegmentation: set_current:', self._options[new_value])
        self._current = self._options[new_value]
        self.notify_observers()

# This will be the shared instance
shared_segmentation = SharedSegmentation()