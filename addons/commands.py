import discord
from discord.ext import commands

class Commands:
    """Server commands."""
    
    @commands.command()
    async def test(self):
        """A test command."""
        await self.bot.send_message(message.channel, 'Testing!')
    
    @commands.command()
    async def restart(self):
        """Restarts the bot."""
        await self.bot.send_message(message.channel, 'Restarting...')
        os.execv(sys.executable, ['python'] + sys.argv)

    @commands.command()
    async def stop(self):
        """Closes the bot."""
        await self.bot.send_message(message.channel, 'Closing...')
        sys.exit()
        
def setup(bot):
    bot.add_cog(Commands())