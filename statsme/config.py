configured = False

recorder = None
record_commands = True
record_uptime = True


class Config:
    def __init__(self):
        self.recorder = recorder
        self.record_commands = record_commands
        self.record_uptime = record_uptime
