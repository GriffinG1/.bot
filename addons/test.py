import pkg_resources
import contextlib
import sys
import inspect
import os
import shutil
import glob
import math
from discord.ext import commands
from io import StringIO
from traceback import format_exc

'''redirection'''


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
        self.stream = io.StringIO()
        self.channel = None

    @commands.command(pass_context=True)
    async def redirect(self, ctx):
        """Redirect STDOUT and STDERR to a channel for debugging purposes."""
        sys.stdout = self.stream
        sys.stderr = self.stream
        self.channel = ctx.message.channel
        await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + "Successfully redirected STDOUT and STDERR to the current channel!")

def setup(bot):
    loop.create_task(debug_cog.redirection_clock())
    bot.add_cog(debug_cog)
