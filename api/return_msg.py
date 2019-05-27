class TokenReturnMsg(object):
    def __init__(self):
        self.code=1000
        self.token=None
        self.error=None
        self.username=None
    @property
    def dict(self):
        return self.__dict__
