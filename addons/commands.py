import discord
import json
from discord.ext import commands
import sys
import os

class Commands:
    """
    Commands for the Nintendo Homebrew Idiot Log server.
    """
    def __init__(self, bot):
        
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    async def simple_embed(self, text, title="", color=discord.Color.default()):
        embed = discord.Embed(title=title, color=color)
        embed.description = text
        await self.bot.say("", embed=embed)

    @commands.command()
    async def test(self):
        """A test command."""
        await self.bot.say("Testing!")
    
    @commands.has_permissions(administrator=True)    
    @commands.command()
    async def restart(self):
        """Restarts the bot."""
        await self.bot.say("Restarting...")
        os.execv(sys.executable, ['python'] + sys.argv)
    
    @commands.has_permissions(administrator=True)   
    @commands.command()
    async def close(self):
        """Ceases execution of the bot."""
        await self.bot.say("Closing...")
        sys.exit()
        
    @commands.command()
    async def log(self, action=False, value=False):
        """Command for managing the bot's internal idiot log, as well as linking the spreadsheet."""
        if action == False:
            await self.bot.say("http://bit.ly/ninidiots")

def setup(bot):
    bot.add_cog(Commands(bot))