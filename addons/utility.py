import discord
from discord.ext import commands
import os
import sys

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
        
def setup(bot):
    bot.add_cog(Utility(bot))