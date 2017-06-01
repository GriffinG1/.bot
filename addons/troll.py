import discord
from discord.ext import commands

class Troll:
    """Commands used for jokes and trolling."""
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
        
    @commands.command()
    async def pm(self, ctx, user, *, message=""):
        """PM's a member since lyrics coding skills are too bad for this."""
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
                    await self.bot.send_message(ctx.message.channel, bot_prefix + 'Invalid user!')
            msg_user = message
            try:
                await self.bot.send_message(member, msg_user)
            except discord.errors.Forbidden: # if Goku is blocked
                pass  
            await self.bot.say("Successfully sent a message to " + user + "!")    
        except discord.errors.Forbidden as e:
            await self.bot.say("An error occurred! " + e)
            
def setup(bot):
    bot.add_cog(Troll(bot))