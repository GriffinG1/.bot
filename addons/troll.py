import discord
from discord.ext import commands

class Troll:
    """Commands used for jokes and trolling."""
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
        
    @commands.command()
    async def pm(self, user, message):
        """PM a specified user."""
        try:
            user = discord.utils.get(server.users, name=user)
            self.bot.send_message(user, message)
        except Exception:
            self.bot.say("Something went wrong! You likely entered an incorrect username.")
            
def setup(bot):
    bot.add_cog(Troll(bot))