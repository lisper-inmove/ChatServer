class MyError(Exception):

    pass


class PopupError(MyError):

    def __init__(self, msg):
        super().__init__(msg)


class PopupSpecError(MyError):

    def __init__(self, errcode, msg):
        super().__init__(msg)
        self.err = [errcode, msg]

    @property
    def msg(self):
        return self.err[1]

    @property
    def code(self):
        return self.err[0]
