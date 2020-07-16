class BaseRecorder:
    """Base recorder that all recorders should inherit from"""

    async def connect(self):
        """Run on cog startup

        Should connect to and prepare the database connection
        This method is optional, and can be left as-is
        """
        pass

    async def disconnect(self):
        """Run on cog unload

        Should disconnect from and cleanup the database connection
        This method is optional, and can be left as-is
        """
        pass

    async def record_commands(self, command_batch):
        """Record a batch of commands into the database

        Each item in the batch is a dict containing the
        following keys and values:

        name: :class:`str`
            The name of the command
        guild: :class:`int`
            The guild id where the command was invoked
        channel: :class:`int`
            The channel id where the command was invoked
        author: :class:`int`
            The author id who invoked the command
        invoked_at: :class:`datetime.datetime`
            The time at which the command was invoked
        prefix: :class:`string`
            The prefix used to invoke the command
        failed: :class:`bool`
            Whether the command failed or not


        Parameters
        -----------
        command_batch: :class:`List[dict]`
            The batch of commands to store
        """
        raise NotImplementedError()

    async def record_messages(self, message_batch):
        raise NotImplementedError()
