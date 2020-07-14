from databases import Database
import sqlalchemy

from .base import BaseRecorder


metadata = sqlalchemy.MetaData()

commands = sqlalchemy.Table(
    "statsme_commands", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, index=True),
    sqlalchemy.Column("guild_id", sqlalchemy.Integer, index=True),
    sqlalchemy.Column("channel_id", sqlalchemy.Integer, index=True),
    sqlalchemy.Column("author_id", sqlalchemy.Integer, index=True),
    sqlalchemy.Column("invoked_at", sqlalchemy.DateTime, index=True),
    sqlalchemy.Column("prefix", sqlalchemy.String),
    sqlalchemy.Column("author_id", sqlalchemy.Boolean, index=True),
)


class DatabasesRecorder(BaseRecorder):
    def __init__(self, database_uri):
        self.db = Database(database_uri)

    async def connect(self):
        await self.db.connect()

    async def disconnect(self):
        await self.db.disconnect()

    async def record_commands(self, command_batch):
        # TODO: this function
        pass
