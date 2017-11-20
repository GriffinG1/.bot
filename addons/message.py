import discord
from discord.ext import commands

class Message:
    """Commands used for jokes and trolling."""
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
    
    def find_user(self, user, ctx):
        found_member = self.bot.guild.get_member_named(user)
        if not found_member:
            try:
                found_member = ctx.message.mentions[0]
            except IndexError:
                pass
        if not found_member:
            found_member = self.bot.guild.get_member(int(user))
        if not found_member:
            return None
        else:
            return found_member
    
    @commands.has_permissions(ban_members=True)    
    @commands.command(aliases=['pm', 'dm'], pass_context=True)
    async def whisper(self, ctx, member, *, message=""):
        """Sends a PM to a specified member."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await ctx.send("That user could not be found.")
        else:
            try:
                await found_member.send(message)
                await ctx.send("Successfully sent a message to {}#{}!".format(found_member.name, found_member.discriminator))    
            except discord.errors.Forbidden: # if Goku is blocked
                await ctx.send("Could not send message. The user likely has the bot blocked.")  
     
    @commands.has_permissions(ban_members=True)       
    @commands.command(pass_context=True)
    async def say(self, ctx, channel, *, msg):
        """Says a message in a specified channel."""
        msg = msg.replace("@everyone", "`@`everyone").replace("@here", "`@`here")
        await ctx.message.channel_mentions[0].send(msg)
        
def setup(bot):
    bot.add_cog(Troll(bot))
