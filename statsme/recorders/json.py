import json
import os

from .base import BaseRecorder

FOLDER_NAME = "statsme_json"
COMMANDS = FOLDER_NAME + "/commands.json"


class JSONRecorder(BaseRecorder):
    """Recorder using python's builtin json module"""
    async def connect(self):
        if not os.path.exists(FOLDER_NAME):
            os.mkdir(FOLDER_NAME)

        if not os.path.isfile(COMMANDS):
            with open(COMMANDS, "w") as f:
                json.dump([], f)

    async def record_commands(self, command_batch):
        with open(COMMANDS, "r") as f:
            commands = json.load(f)

        commands.extend(command_batch)

        with open(COMMANDS, "w") as f:
            json.dump(commands, f, indent=4)
