import discord
from discord.ext import commands

class Troll:
    """Commands used for jokes and trolling."""
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
    
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def pm(self, ctx, user, *, message=""):
        """Sends a PM to a specified member."""
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
            await self.bot.say("Successfully sent a message to {}#{}!".format(member.name, member.discriminator))    
        except discord.errors.Forbidden: # if Goku is blocked
            await self.bot.say("Could not send message. The user likely has the bot blocked.")  
     
    @commands.has_permissions(ban_members=True)       
    @commands.command(pass_context=True)
    async def say(self, ctx, channel, *, msg):
        """Says a message in a specified channel."""
        msg = msg.replace("@everyone", "`@`everyone").replace("@here", "`@`here")
        await self.bot.send_message(ctx.message.channel_mentions[0], msg)
        
def setup(bot):
    bot.add_cog(Troll(bot))
