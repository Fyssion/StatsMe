from discord.ext import commands, menus
import discord

import datetime
import asyncio

from . import config
from .bot_data import BotData
from .config import Config
from .utils.pages import TablePages


class StatsMeBase(commands.Cog):
    """Base cog for StatsMe that contains the commands"""

    load_time = datetime.datetime.now()

    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.now()

        if hasattr(bot, "_statsme_config"):
            self.config = bot._statsme_config

        else:
            self.config = config

        self.recorder = self.config.recorder

        # asyncio setup
        self._data_batch = []
        self._batch_lock = asyncio.Lock(loop=bot.loop)

        self.bot.loop.create_task(self.recorder.connect())

        # add config to bot
        if not hasattr(bot, "_statsme_config"):
            self.bot._statsme_config = Config()

        # add counters to bot
        if not hasattr(bot, "_statsme"):
            start_time = self.start_time if bot.is_ready else None

            bot._statsme = BotData(start_time=start_time)

        self.bot_data = bot._statsme

    async def cog_check(self, ctx):
        # Make sure the author owns the bot
        if not await ctx.bot.is_owner(ctx.author):
            raise commands.NotOwner("You must own this bot to use StatsMe.")
        return True

    def cog_unload(self):
        self.bot.loop.create_task(self.recorder.disconnect())

    # Event listeners

    @commands.Cog.listener()
    async def on_socket_response(self, msg):
        self.bot_data.socket_stats[msg.get("t") or "None"] += 1

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            self.bot_data.messages_sent += 1

        else:
            self.bot_data.messages_recieved += 1

    @commands.Cog.listener()
    async def on_command(self, ctx):
        await self.register_command(ctx)

    async def register_command(self, ctx):
        if ctx.command is None:
            return

        command = ctx.command.qualified_name
        self.bot_data.commands[command] += 1

        message = ctx.message
        if ctx.guild is None:
            guild_id = None
        else:
            guild_id = ctx.guild.id

        async with self._batch_lock:
            self._data_batch.append(
                {
                    "name": command,
                    "guild": guild_id,
                    "channel": ctx.channel.id,
                    "author": ctx.author.id,
                    "invoked_at": message.created_at.isoformat(),
                    "prefix": ctx.prefix,
                    "failed": ctx.command_failed,
                }
            )

    # Commands

    @commands.command(
        description="View websocket stats",
        aliases=["socket", "socketstats", "websocketstats"],
    )
    async def websocket(self, ctx):
        sorted_stats = {}

        for name in sorted(self.bot_data.socket_stats.keys()):
            sorted_stats[name] = self.bot_data.socket_stats[name]

        data = [[n or "None", v] for n, v in sorted_stats.items()]
        data.insert(0, ["Total", sum(self.bot_data.socket_stats.values())])

        source = TablePages(data, title="Websocket Stats")
        pages = menus.MenuPages(source=source, clear_reactions_after=True)
        await pages.start(ctx)


# Based off of jishaku's GroupCogMeta
# https://github.com/Gorialis/jishaku/blob/master/jishaku/metacog.py
class CogGroupMeta(commands.CogMeta):
    def __new__(cls, *args, **kwargs):
        parent = kwargs.pop("parent")

        new_cls = super().__new__(cls, *args, **kwargs)

        for command in new_cls.__cog_commands__:
            if not command.parent:
                command.parent = parent
                command.__original_kwargs__["parent"] = parent

        new_cls.__cog_commands__.append(parent)
        setattr(new_cls, parent.callback.__name__, parent)

        return new_cls
