"""Signal file.  registering, attaching, and raising"""

class Signal(object):
    def __init__(self):
        """Initalize the signals dictionary"""
        self._handlers = []
            
    def emit(self, *args, **kwargs):
        for callback in self._handlers:
            callback(*args, **kwargs)
       
    def connect(self, func):
        self._handlers.append(func)
        return self

    __iadd__ = connect
    __call__ = emit