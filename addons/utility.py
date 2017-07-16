import discord
from discord.ext import commands
import os
import time
import subprocess

class Utility:
    """Utility bot commands."""
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))  
    
    @commands.command()
    async def test(self):
        """A test command."""
        embed = discord.Embed(title="testing", description="Testing")
        embed.add_field(name="Notes", value="Testing!", inline=False)
        embed.colour = discord.Colour(0x00FFFF)            
        await self.bot.say("", embed=embed)
                                                                     
    @commands.has_permissions(ban_members=True)    
    @commands.command()
    async def restart(self):
        """Restarts the bot."""
        await self.bot.say("Restarting...")
        subprocess.Popen(['python3.6', 'run.py'])
        time.sleep(3)
        await self.bot.say("Restarted.")
        time.sleep(99999999999)
        
def setup(bot):
    bot.add_cog(Utility(bot))
