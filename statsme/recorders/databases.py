from databases import Database
import sqlalchemy
from sqlalchemy.schema import CreateTable

from .base import BaseRecorder


raise NotImplementedError("Sorry, this feature is still in development. Try AsyncPGRecorder instead.")


metadata = sqlalchemy.MetaData()

commands = sqlalchemy.Table(
    "statsme_commands",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, index=True),
    sqlalchemy.Column("guild_id", sqlalchemy.Integer, index=True),
    sqlalchemy.Column("channel_id", sqlalchemy.Integer, index=True),
    sqlalchemy.Column("author_id", sqlalchemy.Integer, index=True),
    sqlalchemy.Column("invoked_at", sqlalchemy.DateTime, index=True),
    sqlalchemy.Column("prefix", sqlalchemy.String),
    sqlalchemy.Column("failed", sqlalchemy.Boolean, index=True),
)

tables = [commands]


class DatabasesRecorder(BaseRecorder):
    def __init__(self, database_uri):
        self.db = Database(database_uri)

    async def connect(self):
        await self.db.connect()

        async with self.db.connection() as conn:
            for table in tables:
                create_expr = CreateTable(table)
                await conn.execute(create_expr)

    async def disconnect(self):
        await self.db.disconnect()

    async def record_commands(self, command_batch):
        await self.db.execute(commands.insert(), command_batch)
