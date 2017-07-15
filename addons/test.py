import pkg_resources
import contextlib
import sys
import inspect
import os
import shutil
import appuselfbot
import glob
import math
from PythonGists import PythonGists
from discord.ext import commands
from io import StringIO
from traceback import format_exc
from cogs.utils.checks import *

# Common imports that can be used by the debugger.
import requests
import json
import gc
import datetime
import time
import traceback
import prettytable
import re
import io
import asyncio
import discord
import random
import subprocess
from bs4 import BeautifulSoup
import urllib
import psutil

'''Module for the python interpreter as well as saving, loading, viewing, etc. the cmds/scripts ran with the interpreter.'''


# Used to get the output of exec()
@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


class Testing:

    def __init__(self, bot):
        self.bot = bot
        self.stream = io.StringIO()
        self.channel = None

    @commands.command(pass_context=True)
    async def redirect(self, ctx):
        """Redirect STDOUT and STDERR to a channel for debugging purposes."""
        sys.stdout = self.stream
        sys.stderr = self.stream
        self.channel = ctx.message.channel
        await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + "Successfully redirected STDOUT and STDERR to the current channel!")
