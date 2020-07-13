from discord.ext import commands
import discord

import humanize

from . import config
from .base import StatsMeBase, CogGroupMeta
from .errors import NotConfigured


def configure(*, database_uri, track_messages=False):
    config.SETUP_CONFIG = True

    config.DATABASE_URI = database_uri
    config.TRACK_MESSAGES = track_messages


@commands.group(description="Set of commands for using StatsMe", aliases=["sme"])
async def statsme(self, ctx):
    em = discord.Embed(title="StatsMe Bot Statistics", color=discord.Color.blurple())
    em.add_field(
        name="StatsMe cog stats",
        value=(
            f"• loaded {humanize.naturaltime(self.load_time)}\n"
            f"• started {humanize.naturaltime(self.start_time)}\n"
        ),
    )

    em.add_field(
        name="Bot stats (since boot)",
        value=(
            f"• {sum(self.bot_data.commands.values())} commands used\n"
            f"• {self.bot_data.messages_recieved} messages recieved\n"
            f"• {self.bot_data.messages_sent} messages sent"
            f"• {len(self.bot.guilds)} guilds\n"
            f"• {len(self.bot.users)} users\n"
        ),
    )

    await ctx.send(embed=em)


class StatsMe(StatsMeBase, metaclass=CogGroupMeta, parent=statsme):
    pass


def setup(bot):
    if not config.SETUP_CONFIG:
        raise NotConfigured("You must configure StatsMe before loading the extension.")

    bot.add_cog(StatsMe(bot))
