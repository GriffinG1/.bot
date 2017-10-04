#Importing libraries
import discord
from discord.ext import commands
from sys import argv

class Load:
    """
    Load commands.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    # Load test
    @commands.has_permissions(ban_members=True)
    @commands.command(hidden=True)
    async def load(self, ctx, *, module):
        """Loads an addon"""
        try:
            self.bot.load_extension("addons.{}".format(module))
        except Exception as e:
            await ctx.send(':anger: Failed!\n```\n{}: {}\n```'.format(type(e).__name__, e))
        else:
            await ctx.send(':white_check_mark: Extension loaded.')

    @commands.has_permissions(ban_members=True)
    @commands.command(hidden=True)
    async def unload(self, ctx, *, module):
        """Unloads an addon"""
        try:
            if module == "addons.load":
                await ctx.send(":exclamation: I don't think you want to unload that!")
            else:
            self.bot.unload_extension("addons.{}".format(module))
        except Exception as e:
            await ctx.send(':anger: Failed!\n```\n{}: {}\n```'.format(type(e).__name__, e))
        else:
            await ctx.send(':white_check_mark: Extension unloaded.')
   
    @commands.has_permissions(ban_members=True)
    @commands.command(hidden=True)
    async def reload(self, ctx):
        """Reloads an addon."""
        errors = ""
        for addon in os.listdir("addons"):
            if ".py" in addon:
                cog = cog.replace('.py', '')
                try:
                    self.bot.unload_extension("cogs.{}".format(addon))
                    self.bot.load_extension("cogs.{}".format(addon))
                except Exception as e:
                    errors += 'Failed to load module: `{}.py` due to `{}: {}`\n'.format(addon, type(e).__name__, e)
        if not errors:
            await ctx.send(self.bot.bot_prefix + "All addons reloaded")
        else:
            await ctx.send(self.bot.bot_prefix + errors)

def setup(bot):
    bot.add_cog(Load(bot))
