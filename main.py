description = """Goku, the bot for the Nintendo Homebrew Idiot Log Discord!"""

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

git = git.cmd.Git(".")

prefix = ['!', '.']
bot = commands.Bot(command_prefix=prefix, description=description, pm_help=None)

config = configparser.ConfigParser()
config.read("config.ini")

bot.actions = []  # changes messages in mod-/server-logs


# http://stackoverflow.com/questions/3411771/multiple-character-replace-with-python
def escape_name(name):
    chars = "\\`*_<>#@:~"
    name = str(name)
    for c in chars:
        if c in name:
            name = name.replace(c, "\\" + c)
    return name.replace("@", "@\u200b")  # prevent mentions


bot.escape_name = escape_name
bot.pruning = False  # used to disable leave logs if pruning, maybe.
bot.escape_trans = str.maketrans({
    "*": "\*",
    "_": "\_",
    "~": "\~",
    "`": "\`",
    "\\": "\\\\"
})  # used to escape a string


# mostly taken from https://github.com/Rapptz/discord.py/blob/async/discord/ext/commands/bot.py
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        pass  # ...don't need to know if commands don't exist
    if isinstance(error, discord.ext.commands.errors.CheckFailure):
        await ctx.send("You don't have permission to use this command.")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        formatter = commands.formatter.HelpFormatter()
        await ctx.send("You are missing required arguments.\n{}".format(formatter.format_help_for(ctx, ctx.command)[0]))
    else:
        if ctx.command:
            await ctx.send("An error occurred while processing the `{}` command.".format(ctx.command.name))
        print('Ignoring exception in command {0.command} in {0.message.channel}'.format(ctx))
        tb = traceback.format_exception(type(error), error, error.__traceback__)
        error_trace = "".join(tb)
        print(error_trace)
        embed = discord.Embed(description=error_trace.translate(bot.escape_trans))
        await bot.err_logs_channel.send("An error occurred while processing the `{}` command in channel `{}`.".format(ctx.command.name, ctx.message.channel), embed=embed)


@bot.event
async def on_error(event_method, *args, **kwargs):
    if isinstance(args[0], commands.errors.CommandNotFound):
        return
    print("Ignoring exception in {}".format(event_method))
    tb = traceback.format_exc()
    error_trace = "".join(tb)
    print(error_trace)
    embed = discord.Embed(description=error_trace.translate(bot.escape_trans))
    await bot.err_logs_channel.send("An error occurred while processing `{}`.".format(event_method), embed=embed)

bot.all_ready = False
bot._is_all_ready = asyncio.Event(loop=bot.loop)


async def wait_until_all_ready():
    """Wait until the entire bot is ready."""
    await bot._is_all_ready.wait()
bot.wait_until_all_ready = wait_until_all_ready


@bot.event
async def on_ready():
    # this bot should only ever be in one server anyway
    for guild in bot.guilds:
        bot.guild = guild
        if bot.all_ready:
            break
        bot.idiots_channel = discord.utils.get(guild.channels, name="idiots")
        bot.private_messages_channel = discord.utils.get(guild.channels, name="private-messages")
        bot.rules_channel = discord.utils.get(guild.channels, name="rules")
        bot.logs_channel = discord.utils.get(guild.channels, name="server-logs")
        bot.cmd_logs_channel = discord.utils.get(guild.channels, name="cmd-logs")
        bot.containment_channel = discord.utils.get(guild.channels, name="containment")
        bot.err_logs_channel = discord.utils.get(guild.channels, name="err-logs")
        bot.msg_logs_channel = discord.utils.get(guild.channels, name="msg-logs")
        bot.hidden_channel = discord.utils.get(guild.channels, name="hiddenplace")
        bot.blacklist_channel = discord.utils.get(guild.channels, name="blacklist")
        
        bot.archit_role = discord.utils.get(guild.roles, name="Tech Support")
        bot.idiots_role = discord.utils.get(guild.roles, name="Idiots")
        bot.muted_role = discord.utils.get(guild.roles, name="No Speaking!")
        bot.unhelpful_jerks_role = discord.utils.get(guild.roles, name="Unhelpful Jerks")
        bot.neutron_stars_role = discord.utils.get(guild.roles, name="Neutron Stars")
        bot.server_admin_role = discord.utils.get(guild.roles, name="Server Admins")
        bot.sheet_admin_role = discord.utils.get(guild.roles, name="Sheet Admins")
        bot.support_role = discord.utils.get(guild.roles, name="I NEED SUPPORT")
        bot.derek_role = discord.utils.get(guild.roles, name="DDM")
        
        print("Initialized on {}.".format(guild.name))
        
        bot.all_ready = True
        bot._is_all_ready.set()

        break
    
# loads extensions
addons = [
    'addons.containment',
    'addons.events',
    'addons.load',
    'addons.message',
    'addons.mod',
    #'addons.music', Commented out until music.py is stable
    'addons.rules',
    'addons.utility',
    'addons.warn'
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
bot.run(config['Main']['token'])
