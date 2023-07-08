from chat3 import Chat

import os
import re
import inspect
import asyncio
import importlib.util
from pathlib import Path

from submodules.utils.logger import Logger
from submodules.utils.sys_env import SysEnv
from handlers.base_handler import BaseHandler
from server import Server

logger = Logger()


class HandlerHelper:

    pattern = re.compile('(?!^)([A-Z]+)')

    def __init__(self, directory):
        self.directory = directory
        self.handlers = dict()

    def load_handler(self, path=None):
        """加载所有handler."""
        if path is None:
            root_dir = SysEnv.get(SysEnv.APPROOT)
            path = os.path.join(root_dir, self.directory)
        for root, dirs, files in os.walk(path):
            for directory in dirs:
                self.load_handler(os.path.join(root, directory))
            for _f in files:
                self.load_handler_from_file(os.path.join(root, _f))

    def load_handler_from_file(self, filepath):
        """加载某一个handler."""
        if not filepath.endswith("py"):
            return
        filename = Path(filepath).name
        if filename.startswith(".#"):  # 忽略emacs生成的临时文件
            return
        spec = importlib.util.spec_from_file_location(self.directory, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for attr in module.__dict__.keys():
            if attr.startswith("__"):
                continue
            _handler = module.__dict__.get(attr)
            if not inspect.isclass(_handler):
                continue
            if not issubclass(_handler, BaseHandler):
                continue
            if _handler == BaseHandler:
                continue
            if not hasattr(_handler, 'PN'):
                continue
            pn = getattr(_handler, 'PN')
            for p in pn:
                if p in self.handlers:
                    continue
                self.handlers.update({p: _handler})
            logger.info(f"导入handler: {_handler} {self.handlers}")


if __name__ == "__main__":

    root_path = os.path.dirname(os.path.realpath(__file__))
    SysEnv.set(SysEnv.APPROOT, root_path)

    handler_helper = HandlerHelper("handlers")
    handler_helper.load_handler()

    server = Server(handler_helper.handlers)
    asyncio.get_event_loop().run_until_complete(server.server)
    asyncio.get_event_loop().run_forever()
