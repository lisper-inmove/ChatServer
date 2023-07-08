from base import Base


class BaseHandler(Base):

    def __init__(self, pn, *args, **kargs):
        super().__init__(*args, **kargs)
        self.cpn = pn

    def PN_to_str(self):
        return self.cpn.to_bytes(2).decode()
