from collections import Counter


class BotData:
    def __init__(self, *, start_time=None):
        self.commands = Counter()

        # Messages recieved from others
        # and messages sent by the bot
        self.messages_recieved = 0
        self.messages_sent = 0

        self.start_time = start_time
