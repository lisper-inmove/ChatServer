import struct
from base import Base


class BaseHandler(Base):

    POPUP_ERROR = 0xFFFF
    PING = 0xFFFE

    LOGIN = 0x01
    SIGN_UP = 0x02

    # 创建消息,发聊天内容
    CREATE_MESSAGE = 0x13
    UPDATE_MESSAGE = 0x14
    LIST_MESSAGE = 0x15
    # 创建聊天
    CREATE_CHAT = 0x10
    UPDATE_CHAT = 0x11
    DELETE_CHAT = 0x12
    LIST_CHAT = 0x16

    def __init__(self, pn, *args, **kargs):
        super().__init__(*args, **kargs)
        self.cpn = pn
