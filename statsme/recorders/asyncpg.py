import asyncpg

from .base import BaseRecorder


commands_sql = """CREATE TABLE IF NOT EXISTS statsme_commands(
                         id INT PRIMARY KEY,
                         name TEXT,
                         guild_id BIGINT
                         channel_id BIGINT
                         author_id BIGINT
                         invoked_at TIMESTAMP
                         prefix TEXT
                         failed BOOLEAN);

                  CREATE INDEX IF NOT EXISTS commands_name_idx ON statsme_commands (name);
                  CREATE INDEX IF NOT EXISTS commands_guild_id_idx ON statsme_commands (guild_id);
                  CREATE INDEX IF NOT EXISTS commands_channel_id_idx ON statsme_commands (channel_id);
                  CREATE INDEX IF NOT EXISTS commands_author_id_idx ON statsme_commands (author_id);
                  CREATE INDEX IF NOT EXISTS commands_invoked_at_idx ON statsme_commands (invoked_at);
               """


class AsyncPGRecorder(BaseRecorder):
    """Represents a recorder for asyncpg"""
    def __init__(self, *args, **kwargs):
        self.pool = None
        self.pool_args = args
        self.poool_kwargs = kwargs

    async def connect(self):
        self.pool = await asyncpg.create_pool(*self.pool_args, **self.poool_kwargs)

        await self.pool.execute(commands_sql)

    async def disconnect(self):
        await self.pool.close()

    async def record_commands(self, command_batch):
        query = """INSERT INTO commands (name, guild_id, channel_id, author_id, invoked_at, prefix, failed)
                   SELECT x.name, x.guild, x.channel, x.author, x.invoked_at, x.prefix, x.failed
                   FROM jsonb_to_recordset($1::jsonb) AS
                   x(name TEXT, guild BIGINT, channel BIGINT, author BIGINT, invoked_at TIMESTAMP, prefix TEXT, failed BOOLEAN)
                """

        await self.pool.execute(query, command_batch)
