import struct
from base import Base


class BaseHandler(Base):

    def __init__(self, pn, *args, **kargs):
        super().__init__(*args, **kargs)
        self.cpn = pn
