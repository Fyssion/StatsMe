from discord.ext import commands
import discord

import humanize
import psutil
import sys
import pkg_resources

from . import config, __version__
from .base import StatsMeBase, CogGroupMeta
from .errors import NotConfigured
from .recorders.base import BaseRecorder
from .utils.tabulate import tabulate


def configure(*, recorder, track_messages=False):
    config.SETUP_CONFIG = True

    config.RECORDER = recorder
    if not isinstance(recorder, BaseRecorder):
        raise TypeError("'recorder' must subclass 'recorders.base.BaseRecorder'")

    config.TRACK_MESSAGES = track_messages


@commands.group(description="Set of commands for using StatsMe", aliases=["sme"])
async def statsme(self, ctx):
    em = discord.Embed(title="StatsMe Bot Statistics", color=discord.Color.blurple())
    em.description = (
        f"Module was loaded {humanize.naturaltime(self.load_time)}\n"
        f"Cog was loaded {humanize.naturaltime(self.start_time)}"
    )

    # Bot stats

    latency = self.bot.latency * 1000

    data = [
        ["Commands used", sum(self.bot_data.commands.values())],
        ["Messages recieved", self.bot_data.messages_recieved],
        ["Messages sent", self.bot_data.messages_sent],
        ["Websocket latency", f"{latency:.2f}ms"]
    ]

    table = tabulate(data, codeblock=True, language="asciidoc")

    em.add_field(name="Bot stats (since boot)", value=table)

    em.add_field(name="\u200b", value="\u200b")

    # Account stats

    channel_count = 0

    for channel in self.bot.get_all_channels():
        channel_count += 1

    data = [
        ["Guilds", len(self.bot.guilds)],
        ["Users", len(self.bot.users)],
        ["Channels", channel_count],
    ]

    table = tabulate(data, codeblock=True)

    em.add_field(name="Account stats", value=table)

    # Process Stats

    try:
        process = psutil.Process()

        memory_usage = process.memory_full_info().uss / 1024**2
        cpu_usage = process.cpu_percent() / psutil.cpu_count()
        pid = f"{process.name()} ({process.pid})"
        threads = process.num_threads()

    except psutil.AccessDenied:
        value = ":exclamation: Missing access rights"

    else:
        data = [
            ["CPU", f"{cpu_usage}%"],
            ["Memory", humanize.naturalsize(memory_usage)],
            ["PID", f"{pid}"],
            ["Threads", threads],
        ]

        value = tabulate(data, codeblock=True, language="asciidoc")

    em.add_field(name="Process stats", value=value)

    # System stats

    vi = sys.version_info
    python_version = f"{vi.major}.{vi.minor}.{vi.micro}"

    try:
        dpy_version = pkg_resources.get_distribution('discord.py').version

    except (pkg_resources.DistributionNotFound, AttributeError):
        dpy_version = discord.__version__

    data = [
        ["OS", sys.platform],
        ["Python version", python_version],
        ["discord.py version", dpy_version],
        ["StatsMe version", __version__],
    ]

    table = tabulate(data, codeblock=True, language="asciidoc")

    em.add_field(name="System stats", value=table, inline=False)

    await ctx.send(embed=em)


class StatsMe(StatsMeBase, metaclass=CogGroupMeta, parent=statsme):
    pass


def setup(bot):
    if not config.SETUP_CONFIG:
        raise NotConfigured("You must configure StatsMe before loading the extension.")

    bot.add_cog(StatsMe(bot))
