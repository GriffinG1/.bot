import discord
from discord.ext import commands

class Troll:
    """Commands used for jokes and trolling."""
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
        
    @commands.command(pass_context=True)
    async def pm(self, ctx, user, *, message=""):
        """Sends a PM to a specified member."""
        try:
            subMsg = ctx.message.content.split(" ")[1]
            memberName = subMsg.strip()
            if memberName:
                try:
                    member = ctx.message.mentions[0]
                except:
                    member = ctx.message.server.get_member_named(memberName)
                if not member:
                    member = ctx.message.server.get_member(memberName)
                if not member:
                    await self.bot.send_message(ctx.message.channel, 'Invalid user!')
            try:
                await self.bot.send_message(member, message)
            except discord.errors.Forbidden: # if Goku is blocked
                await self.bot.say("Could not send message. The user likely has the bot blocked.")  
            await self.bot.say("Successfully sent a message to " + user + "!")    
        except discord.errors.Forbidden as e:
            await self.bot.say("An error occurred! " + e)
            
def setup(bot):
    bot.add_cog(Troll(bot))