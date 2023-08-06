class BObject(object):
    def __init__(self):
        self.Init()

    def Init(self):
        self._ = None

    def Get(self):
        return self._