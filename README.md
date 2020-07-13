# StatsMe

Statistics tracking cog for discord.py bots

Insipred by and based off of [jishaku](https://github.com/Gorialis/jishaku)

## Note

StatsMe is currently in the planning stage.
Everything you see here is subject to change.

## Example

A quick and basic example for StatsMe

```py
from discord.ext import commands
import discord

import statsme


bot = commands.Bot(command_prefix="$")

# Congifure and load StatsMe
statsme.configure(database_uri="database_uri_here")
bot.load_extension("statsme")

bot.run("token_here")
```
