# StatsMe

Statistics tracking cog for discord.py bots

Insipred by and based off of [jishaku](https://github.com/Gorialis/jishaku) and [discord.ext.science](https://github.com/NCPlayz/discord-ext-science)

## Note

StatsMe is currently in the planning stage.
Everything you see here is subject to change.

## Recorders

| Recorder   | Install                          | Source                                                         |
|------------|----------------------------------|----------------------------------------------------------------|
| json       | None                             | [json](https://github.com/python/cpython/tree/master/Lib/json) |
| databases  | `pip install StatsMe[databases]` | [encode/databases](https://github.com/encode/databases)        |
| asyncpg    | `pip install StatsMe[asyncpg]`   | [MagicStack/asyncpg](https://github.com/MagicStack/asyncpg)    |

[databases](https://github.com/encode/databases) (with specified driver) -
for use with `statsme.recorders.databases.DatabasesRecorder`

## Example

A quick and basic example for StatsMe

```py
from discord.ext import commands
import discord

import statsme
from statsme.recorders.databases import DatabasesRecorder


bot = commands.Bot(command_prefix="$")

# Congifure and load StatsMe
statsme.configure(recorder=DatabasesRecorder("database-uri-here"))
bot.load_extension("statsme")

bot.run("token_here")
```
