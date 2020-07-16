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


def configure(*, recorder, record_commands=True, record_uptime=True):
    """Configure StatsMe

    This MUST be run before loading statsme as an extension

    Parameters
    -----------
    recorder: :class:`statsme.recorders.base.BaseRecorder`
        The recorder to use for saving data
    record_commands: Optional[:class:`bool`]
        Whether to record commands run. Default is True
    record_uptime: Optionl[:class:`bool`]
        Whether to record uptime stats. Default is True

    Raises
    -------
    :class:`TypeError`
        When the recorder is not an instance or does not subclass
        :class:`statsme.recorders.base.BaseRecorder`
    """
    config.configured = True

    config.recorder = recorder
    if not isinstance(recorder, BaseRecorder):
        raise TypeError("'recorder' must subclass 'recorders.base.BaseRecorder'")

    config.record_commands = record_commands
    config.record_uptime = record_uptime


@commands.group(
    description="Set of subcommands for using StatsMe",
    aliases=["sme"],
    invoke_without_command=True,
)
async def statsme(self, ctx):
    em = discord.Embed(title="StatsMe Bot Statistics", color=discord.Color.blurple())
    em.description = (
        f"Module was loaded {humanize.naturaltime(self.load_time)}\n"
        f"Cog was loaded {humanize.naturaltime(self.start_time)}"
    )

    # Bot stats

    latency = self.bot.latency * 1000

    socket_responses = humanize.intword(sum(self.bot_data.socket_stats.values()))

    data = [
        ["Commands used", sum(self.bot_data.commands.values())],
        ["Messages recieved", self.bot_data.messages_recieved],
        ["Messages sent", self.bot_data.messages_sent],
        ["Websocket latency", f"{latency:.2f}ms"],
        ["Socket responses", socket_responses,],
    ]

    table = tabulate(data, codeblock=True, language="asciidoc")

    em.add_field(name="Bot stats (since boot)", value=table)

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

        memory_usage = process.memory_full_info().uss / 1024 ** 2
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

    em.add_field(name="Process stats", value=value, inline=False)

    # System stats

    vi = sys.version_info
    python_version = f"{vi.major}.{vi.minor}.{vi.micro}"

    try:
        dpy_version = pkg_resources.get_distribution("discord.py").version

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
    if hasattr(bot, "_statsme_config"):
        pass

    elif not config.configured:
        raise NotConfigured("You must configure StatsMe before loading the extension.")

    bot.add_cog(StatsMe(bot))
