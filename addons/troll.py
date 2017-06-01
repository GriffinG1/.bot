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
            user = get_member_named(user)
            self.bot.send_message(user, message)
        except Exception:
            self.bot.say("Invalid user!")
            
def setup(bot):
    bot.add_cog(Troll(bot))