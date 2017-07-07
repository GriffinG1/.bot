description = """
Goku, the bot for the Nintendo Homebrew Idiot Log Discord!
"""

# import dependencies
import os
from discord.ext import commands
import discord
import datetime
import json, asyncio
import copy
import configparser
import traceback
import sys
import os
import re
import json
import ast
import git

# sets working directory to bot's folder
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

the_filename = "customcmds.txt"
git = git.cmd.Git(".")

with open(the_filename) as f:
    comms = json.loads(f.readline().strip())

prefix = ['!', '.']
bot = commands.Bot(command_prefix=prefix, description=description, pm_help=None)

bot.actions = []  # changes messages in mod-/server-logs

# http://stackoverflow.com/questions/3411771/multiple-character-replace-with-python
chars = "\\`*_<>#@:~"
def escape_name(name):
    name = str(name)
    for c in chars:
        if c in name:
            name = name.replace(c, "\\" + c)
    return name.replace("@", "@\u200b")  # prevent mentions
bot.escape_name = escape_name

bot.pruning = False  # used to disable leave logs if pruning, maybe.

# mostly taken from https://github.com/Rapptz/discord.py/blob/async/discord/ext/commands/bot.py
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        pass  # ...don't need to know if commands don't exist
    if isinstance(error, discord.ext.commands.errors.CheckFailure):
        await bot.send_message(ctx.message.channel, "{} You don't have permission to use this command.".format(ctx.message.author.mention))
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        formatter = commands.formatter.HelpFormatter()
        await bot.send_message(ctx.message.channel, "{} You are missing required arguments.\n{}".format(ctx.message.author.mention, formatter.format_help_for(ctx, ctx.command)[0]))
    else:
        if ctx.command:
            await bot.send_message(ctx.message.channel, "An error occured while processing the `{}` command.".format(ctx.command.name))
        print('Ignoring exception in command {}'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

bot.all_ready = False
bot._is_all_ready = asyncio.Event(loop=bot.loop)
async def wait_until_all_ready():
    """Wait until the entire bot is ready."""
    await bot._is_all_ready.wait()
bot.wait_until_all_ready = wait_until_all_ready

@bot.event
async def on_ready():
    # this bot should only ever be in one server anyway
    for server in bot.servers:
        bot.server = server
        if bot.all_ready:
            break
        bot.idiots_channel = discord.utils.get(server.channels, name="idiots")
        bot.private_messages_channel = discord.utils.get(server.channels, name="private-messages")
        bot.rules_channel = discord.utils.get(server.channels, name="rules")
        bot.logs_channel = discord.utils.get(server.channels, name="logs")
        
        bot.archit_role = discord.utils.get(server.roles, name="Tech Support")
        bot.idiots_role = discord.utils.get(server.roles, name="Idiots")
        print("Initialized on {}.".format(server.name))
        
        bot.all_ready = True
        bot._is_all_ready.set()

        break
    
# loads extensions
addons = [
    'addons.utility',
    'addons.customcmds',
    'addons.load',
    'addons.troll',
    'addons.log',
    'addons.events'
]

failed_addons = []

for extension in addons:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print('{} failed to load.\n{}: {}'.format(extension, type(e).__name__, e))
        failed_addons.append([extension, type(e).__name__, e])


# Execute
print('Bot directory: ', dir_path)
bot.run("MzE2MDI3ODc4NjAzMDk2MDY1.DAPTiQ.7QG9qND8pAJWsvPcGuVqWmG2H3I")
# MzE2MDI3ODc4NjAzMDk2MDY1.DAPTiQ.7QG9qND8pAJWsvPcGuVqWmG2H3I is stable
# MzI0MDQ5NTIyNDMyOTMzODg4.DCECKg.aqDI02VcJm5BP36nhwarF0DWCXI is beta