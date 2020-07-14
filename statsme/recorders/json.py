import json

from .base import BaseRecorder


class JSONRecorder(BaseRecorder):
    def __init__(self, file):
        self.file = file

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def record_commands(self):
        pass
