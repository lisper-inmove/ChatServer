class MyError(Exception):

    pass


class PopupError(MyError):

    def __init__(self, msg):
        super().__init__(msg)
